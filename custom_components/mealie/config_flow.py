"""Adds config flow for Mealie."""
from __future__ import annotations
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_HOST
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import homeassistant.helpers.config_validation as cv
from .api import MealieApi
from .const import CONF_ENTRIES, CONST_ENTRIES, DOMAIN, NAME


class MealieFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for mealie."""

    VERSION = 1

    _connection_data: dict[str, Any] = {}

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""

        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self: config_entries.ConfigFlow, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors: dict[str, Any] = {}

        if user_input is not None:
            valid = await self._test_credentials(user_input)
            if valid:
                self._connection_data = user_input
                return await self.async_step_options()

            errors["base"] = "invalid_auth"

        data_schema = {
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        }

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=errors
        )

    async def async_step_options(
        self: config_entries.ConfigFlow, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:
            return self.async_create_entry(
                title=NAME, data=self._connection_data, options=user_input
            )

        data_schema = {
            vol.Optional(CONF_ENTRIES, default=CONST_ENTRIES): cv.multi_select(
                CONST_ENTRIES
            ),
        }

        return self.async_show_form(
            step_id="options", data_schema=vol.Schema(data_schema)
        )

    async def _test_credentials(self, options: dict[str, str]):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = MealieApi(
                options[CONF_USERNAME],
                options[CONF_PASSWORD],
                options[CONF_HOST],
                session,
            )
            await client.async_get_api_app_about()
            return True
        except Exception:  # pylint: disable=broad-except
            return False


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self: config_entries.OptionsFlow, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options step."""

        if user_input is not None:
            return self.async_create_entry(title=NAME, data=user_input)

        data_schema = {
            vol.Optional(
                CONF_ENTRIES,
                default=self.config_entry.options.get(CONF_ENTRIES, CONST_ENTRIES),
            ): cv.multi_select(CONST_ENTRIES),
        }
        return self.async_show_form(step_id="init", data_schema=vol.Schema(data_schema))
