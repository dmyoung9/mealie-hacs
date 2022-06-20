"""Sensor platform for Mealie."""
from homeassistant.components.camera import Camera
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import CONF_USERNAME, CONF_HOST

from .const import DEFAULT_NAME
from .const import ATTRIBUTION
from .const import CAMERA
from .const import DOMAIN
from .const import NAME

ICONS = {
    "breakfast": "mdi:egg-fried",
    "lunch": "mdi:bread-slice",
    "dinner": "mdi:pot-steam",
    "side": "mdi:bowl-mix-outline",
}


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            MealPlanCamera(meal, coordinator, entry)
            for meal in ["breakfast", "lunch", "dinner", "side"]
        ]
    )


class MealieCamera(Camera):
    """mealie Camera class."""

    def __init__(self, meal, coordinator, config_entry):
        super().__init__()
        self.coordinator = coordinator
        self.config_entry = config_entry
        self.api = self.coordinator.api
        self.endpoint = "groups/mealplans/today"
        self.meal = meal

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{self.endpoint}_{self.meal}"

    @property
    def device_info(self):
        about_data = self.coordinator.data.get("app/about")
        config_data = self.config_entry.data
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": str(config_data.get(CONF_USERNAME)),
            "model": str(about_data.get("version")),
            "manufacturer": NAME,
            "configuration_url": str(config_data.get(CONF_HOST)),
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }

    @property
    def name(self):
        """Return the name of the camera."""
        return f"{DEFAULT_NAME}_{CAMERA}"

    @property
    def icon(self):
        """Return the icon of the camera."""
        return ICONS.get(self.meal)

    @property
    def device_class(self):
        """Return de device class of the camera."""
        return "mealie__custom_device_class"


class MealPlanCamera(MealieCamera):
    @property
    def name(self):
        return f"Today's {self.meal.title()}"

    @property
    def available(self):
        return True

    @property
    def state(self):
        mealplans = self.coordinator.data.get(self.endpoint, {})
        recipes = [i['recipe'] for i in mealplans if i['entryType'] == self.meal]
        if recipes:
            recipe = recipes[0]

            return recipe['name']

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        mealplans = self.coordinator.data.get(self.endpoint, {})
        recipes = [i['recipe'] for i in mealplans if i['entryType'] == self.meal]
        if recipes:
            recipe = recipes[0]

            return await self.coordinator.api.async_get_api_media_recipes_images(
                recipe['id']
            )

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        return None
