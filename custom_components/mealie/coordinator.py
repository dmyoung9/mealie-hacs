from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, UPDATE_INTERVAL
from .api import MealieApi
from .models import About, MealPlan, MealieData


class MealieDataUpdateCoordinator(DataUpdateCoordinator[MealieData]):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: MealieApi,
    ) -> None:
        """Initialize."""
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)
        self.api = client
        self.platforms = []

    async def _async_update_data(self) -> MealieData:
        """Update data via library."""

        try:
            data = MealieData()

            data.about = About.parse_obj(await self.api.async_get_api_app_about())

            mealplans = await self.api.async_get_api_groups_mealplans_today()

            for mealplan in mealplans:
                data.mealPlans.append(MealPlan.parse_obj(mealplan))

            return data
        except Exception as exception:
            LOGGER.exception(exception)
            raise UpdateFailed() from exception

    async def async_load_recipe_img(self, recipe_id: str) -> bytes:
        """Load an image for a recipe."""

        return await self.api.async_get_api_media_recipes_images(recipe_id)
