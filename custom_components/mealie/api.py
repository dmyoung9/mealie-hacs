from __future__ import annotations

import asyncio
import json
import logging
import socket
from typing import Any

import aiohttp
import async_timeout

from config.custom_components.mealie.models import About, MealPlan, MealieData

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)


class MealieError(Exception):
    """Mealie error."""


class MealieApi:
    """Wrapper for Mealie's API."""

    def __init__(
        self, username: str, password: str, host: str, session: aiohttp.ClientSession
    ) -> None:
        self._session = session

        self._host = host
        self._username = username
        self._password = password

        self._headers = {
            "Content-type": "application/json; charset=UTF-8",
            "Accept": "application/json",
        }

    async def request(
        self, uri: str, method: str = "GET", headers={}, skip_auth=False, data={}
    ) -> dict[str, Any]:
        """Handle a request to the Mealie instance"""
        url = f"{self._host}/api/{uri}"

        if self._session is None:
            self._session = aiohttp.ClientSession()
            # self._close_session = True

        if not skip_auth and self._headers.get("Authorization") is None:
            await self.async_get_api_auth_token()

        headers = self._headers | headers

        try:
            async with async_timeout.timeout(TIMEOUT):
                response = await self._session.request(
                    method=method, url=url, data=data, headers=headers
                )

        except asyncio.TimeoutError as exception:
            raise MealieError(
                "Timeout occurred while connecting to the Mealie API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise MealieError(
                "Error occurred while communicating with Mealie."
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if response.status // 100 in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise MealieError(response.status, json.loads(contents.decode("utf8")))
            raise MealieError(response.status, {"message": contents.decode("utf8")})

        if "application/json" in content_type:
            return await response.json()

        text = await response.text()
        return {"message": text}

    async def async_get_api_app_about(self) -> About:
        """Get data from the API."""
        response = await self.request("admin/about")
        return About.parse_obj(response)

    async def async_get_api_groups_mealplans_today(self) -> list[MealPlan]:
        """Get today's mealplan from the API."""
        response = await self.request("groups/mealplans/today")
        return [MealPlan.parse_obj(mealplan) for mealplan in response]

    # async def async_get_api_media_recipes_images(self, recipe_id) -> bytes:
    #     """Get the image for a recipe from the API."""
    #     filename = "min-original.webp"
    #     url = f"media/recipes/{recipe_id}/images/{filename}"
    #     return await self.request(
    #         url, headers={"Content-type": "image/webp"}, as_bytes=True
    #     )

    async def async_get_api_auth_token(self) -> str:
        """Gets an access token from the API."""
        payload = {
            "username": self._username,
            "password": self._password,
            "grant_type": "password",
        }

        response = await self.request(
            "auth/token",
            method="POST",
            data=payload,
            headers={"Content-type": "application/x-www-form-urlencoded"},
            skip_auth=True,
        )

        access_token = response.get("access_token")
        self._headers["Authorization"] = f"Bearer {access_token}"
        return {"Authorization": f"Bearer {access_token}"}
