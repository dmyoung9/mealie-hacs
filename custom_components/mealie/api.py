"""Sample API Client."""
import asyncio
import logging
import socket
from urllib.parse import urlencode

import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)


class MealieApiClient:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        session: aiohttp.ClientSession,
        token: str = None,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._host = host
        self._token = token
        self._session = session
        self._headers = {
            "Content-type": "application/json; charset=UTF-8",
            "Accept": "application/json",
        }
        if self._token is not None:
            self._headers["Authorization"] = f"Bearer {self._token}"

    async def async_get_api_app_about(self) -> dict:
        """Get data from the API."""
        url = "app/about"
        return await self.api_wrapper("get", url)

    async def async_get_api_groups_mealplans_today(self) -> dict:
        url = "groups/mealplans/today"
        return await self.api_wrapper("get", url)

    async def async_get_api_media_recipes_images(self, recipe_id):
        filename = "min-original.webp"
        url = f"media/recipes/{recipe_id}/images/{filename}"
        return await self.api_wrapper(
            "get", url, headers={"Content-type": "image/webp"}, bytes=True
        )

    async def async_set_title(self, value: str) -> None:
        """Get data from the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        await self.api_wrapper(
            "patch", url, data={"title": value}, headers=self._headers
        )

    async def async_get_token(self) -> str:
        """Gets an access token from the API."""
        url = f"{self._host}/api/auth/token"
        payload = urlencode(
            {
                "username": self._username,
                "password": self._password,
                "grant_type": "password",
            }
        )

        response = await self._session.post(
            url,
            data=payload,
            headers={"Content-type": "application/x-www-form-urlencoded"},
        )
        data = await response.json()
        access_token = data.get("access_token")
        self._headers["Authorization"] = f"Bearer {access_token}"
        return self._headers

    async def api_wrapper(
        self,
        method: str,
        url: str,
        data: dict = {},
        headers: dict = {},
        bytes: bool = False,
    ) -> dict:
        """Get information from the API."""
        if self._token is None:
            headers = await self.async_get_token()
        url = f"{self._host}/api/{url}"
        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await (response.read() if bytes else response.json())

                elif method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post":
                    await self._session.post(url, headers=headers, json=data)

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
