"""MealieEntity class"""
from __future__ import annotations

import time

from homeassistant.const import CONF_HOST, CONF_USERNAME
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ICONS, NAME

from .coordinator import MealieDataUpdateCoordinator


class MealieEntity(CoordinatorEntity[MealieDataUpdateCoordinator]):
    """mealie Entity class."""

    def __init__(self, coordinator: MealieDataUpdateCoordinator) -> None:
        """Initialize the Mealie entity"""
        super().__init__(coordinator)

        self._attr_unique_id = self.coordinator.config_entry.entry_id

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name=self.coordinator.config_entry.data.get(CONF_USERNAME),
            sw_version=self.coordinator.data.about.version,
            manufacturer=NAME,
            configuration_url=self.coordinator.config_entry.data.get(CONF_HOST),
            suggested_area="Kitchen",
            entry_type=DeviceEntryType.SERVICE,
        )


class MealPlanEntity(MealieEntity):
    """mealie Meal Plan Entity class."""

    def __init__(self, meal, coordinator, config_entry):
        super().__init__(coordinator, config_entry)
        self.config_entry = config_entry
        self.endpoint = "groups/mealplans/today"
        self.meal = meal
        self.idx = None
        self.recipes = []

    @property
    def name(self):
        return f"Meal Plan {self.meal.title()}"

    @property
    def icon(self):
        """Return the icon of the camera."""
        return ICONS.get(self.meal)

    def _get_recipes(self):
        mealplans = self.coordinator.data.get(self.endpoint, {})
        self.recipes = [i["recipe"] for i in mealplans if i["entryType"] == self.meal]
        self.idx = self._get_time_based_index()

    def _get_time_based_index(self, interval=60):
        return round(
            ((int(time.time()) % interval) / interval) * (len(self.recipes) - 1)
        )

    async def async_update(self):
        self._get_recipes()

    async def async_added_to_hass(self) -> None:
        self._get_recipes()
