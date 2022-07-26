"""Sensor platform for Mealie."""
from __future__ import annotations

from .coordinator import MealieDataUpdateCoordinator

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.core import callback

from .const import DOMAIN
from .const import UPDATE
from .entity import MealieEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator: MealieDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([MealieUpdate(coordinator)])


class MealieUpdate(MealieEntity, UpdateEntity):
    """mealie Update class."""

    def __init__(self, coordinator: MealieDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        UpdateEntity.__init__(self)

        self._latest_version = None
        self._release_url = None
        self._release_notes = None

        self._attr_unique_id = UPDATE
        # self._attr_supported_features = UpdateEntityFeature.

        self._process_update()

    @callback
    def _process_update(self) -> None:
        """Handle updated data from the coordinator."""

        if self.coordinator.data.about is not None:
            self._attr_installed_version = self.coordinator.data.about.version
            # self._attr_latest_version = self.coordinator.data.about.versionLatest
