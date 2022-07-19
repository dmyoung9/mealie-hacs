"""MealieEntity class"""
from __future__ import annotations

from .models import Recipe

from homeassistant.const import CONF_HOST, CONF_USERNAME
from homeassistant.core import callback
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

    def __init__(self, meal, coordinator):
        super().__init__(
            coordinator,
        )

        self._attr_unique_id = meal

        self.meal = meal
        self.recipe: Recipe | None = None

    @property
    def name(self):
        return None if not self.recipe else self.recipe.name

    @property
    def icon(self):
        """Return the icon of the camera."""
        return ICONS.get(self.meal)

    @property
    def native_value(self):
        return None if not self.recipe else self.recipe.name

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.recipe = next(
            (
                mealPlan.recipe
                for mealPlan in self.coordinator.data.mealPlans
                if mealPlan.entryType == self.meal
            ),
            None,
        )

        self.async_write_ha_state()
