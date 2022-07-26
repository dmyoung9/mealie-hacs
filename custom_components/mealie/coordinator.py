from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_INCLUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MealieApi
from .const import (
    CONST_INCLUDE_ASSETS,
    CONST_INCLUDE_COMMENTS,
    CONST_INCLUDE_EXTRAS,
    CONST_INCLUDE_INSTRUCTIONS,
    CONST_INCLUDE_NOTES,
    CONST_INCLUDE_NUTRITION,
    DOMAIN,
    LOGGER,
    UPDATE_INTERVAL,
)
from .models import About, MealieData, MealPlan


class MealieDataUpdateCoordinator(DataUpdateCoordinator[MealieData]):
    """Class to manage fetching data from the API."""

    def __init__(
        self, hass: HomeAssistant, client: MealieApi, entry: ConfigEntry
    ) -> None:
        """Initialize."""
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)
        self.api = client
        self.platforms = []

        extra_request_options = [
            CONST_INCLUDE_INSTRUCTIONS,
            CONST_INCLUDE_NUTRITION,
            CONST_INCLUDE_COMMENTS,
            CONST_INCLUDE_EXTRAS,
            CONST_INCLUDE_NOTES,
            CONST_INCLUDE_ASSETS,
        ]

        entry_options = entry.options.get(CONF_INCLUDE, [])

        self.needs_additional_requests = any(
            item in entry_options for item in extra_request_options
        )

    async def _async_update_data(self) -> MealieData:
        """Update data via library."""

        try:
            data = MealieData()

            data.about = About.parse_obj(await self.api.async_get_api_app_about())

            mealplans = await self.api.async_get_api_groups_mealplans_today()

            for mealplan in mealplans:
                meal_plan = MealPlan.parse_obj(mealplan)

                # Request the dedicated recipe endpoint if we need more info
                if self.needs_additional_requests and meal_plan.recipe is not None:
                    meal_plan.recipe = await self.api.async_get_api_recipe(
                        meal_plan.recipe.slug
                    )

                data.mealPlans.append(meal_plan)

            return data
        except Exception as exception:
            LOGGER.exception(exception)
            raise UpdateFailed() from exception
