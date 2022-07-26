"""Sensor platform for Mealie."""
from __future__ import annotations

from homeassistant.components.camera import Camera
from homeassistant.const import CONF_HOST
from homeassistant.core import callback
from homeassistant.helpers.httpx_client import get_async_client

from .const import CONF_ENTRIES, DOMAIN
from .coordinator import MealieDataUpdateCoordinator
from .entity import MealPlanEntity

GET_IMAGE_TIMEOUT = 10


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator: MealieDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [MealPlanCamera(meal, coordinator) for meal in entry.options[CONF_ENTRIES]]
    )


class MealPlanCamera(MealPlanEntity, Camera):
    """mealie Camera class."""

    def __init__(self, meal, coordinator: MealieDataUpdateCoordinator):
        self._old_recipe_id: str | None = None

        self._needs_refresh = False
        self._recipe_img: bytes | None
        self._media_url: str | None = None

        super().__init__(meal, coordinator)
        Camera.__init__(self)

    @callback
    def _process_update(self) -> None:
        super()._process_update()

        if (
            self.recipe is not None
            and self.recipe.image
            and (self.recipe.id is not self._old_recipe_id)
        ):
            self._old_recipe_id = self.recipe.id

            self._media_url = f"{self.coordinator.config_entry.data.get(CONF_HOST)}/api/media/recipes/{self.recipe.id}/images/min-original.webp"

            self._needs_refresh = True

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        if self.recipe is None or self.recipe.image is None:
            return None

        if self._needs_refresh and self._media_url is not None:
            async_client = get_async_client(self.hass)
            response = await async_client.get(
                self._media_url, timeout=GET_IMAGE_TIMEOUT
            )
            response.raise_for_status()
            self._recipe_img = response.content

        return self._recipe_img
