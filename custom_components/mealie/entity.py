"""MealieEntity class"""
from homeassistant.const import CONF_HOST, CONF_USERNAME
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import DOMAIN
from .const import NAME


class MealieEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.endpoint = "app/about"
        self.api = self.coordinator.api

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        about_data = self.coordinator.data.get("app/about")
        config_data = self.config_entry.data
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
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
