"""Sensor platform for Mealie."""
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SENSOR
from .entity import MealieEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([MealPlanSensor(coordinator, entry)])


class MealieSensor(MealieEntity):
    """mealie Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("body")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "mealie__custom_device_class"


class MealPlanSensor(MealieSensor):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator, config_entry)
        self.endpoint = "groups/mealplans/today"

    @property
    def name(self):
        return "Today's Meal Plan"

    @property
    def state(self):
        mealplans = self.coordinator.data.get(self.endpoint, {})
        recipe = [i['recipe'] for i in mealplans if i['entryType'] == "dinner"]
        if recipe:
            recipe = recipe[0]

        return recipe['name']
