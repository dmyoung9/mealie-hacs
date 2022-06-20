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

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": str(self.config_entry.data.get(CONF_USERNAME)),
            "model": str(self.coordinator.data.get("version")),
            "manufacturer": NAME,
            "configuration_url": str(self.config_entry.data.get(CONF_HOST)),
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": DOMAIN,
        }
