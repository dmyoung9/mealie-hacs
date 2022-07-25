"""Constants for Mealie."""
# Base component constants
from datetime import timedelta
import logging
from typing import Final


NAME = "Mealie"
DOMAIN = "mealie"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.0"

LOGGER = logging.getLogger(__package__)

UPDATE_INTERVAL = timedelta(seconds=30)

CONF_ENTRIES = "entries"

CONST_ENTRY_BREAKFAST = "breakfast"
CONST_ENTRY_LUNCH = "lunch"
CONST_ENTRY_DINNER = "dinner"
CONST_ENTRY_SIDE = "side"

CONST_ENTRIES: Final = [
    CONST_ENTRY_BREAKFAST,
    CONST_ENTRY_LUNCH,
    CONST_ENTRY_DINNER,
    CONST_ENTRY_SIDE,
]


ISSUE_URL = "https://github.com/mealie-recipes/mealie-hacs/issues"
SOURCE_REPO = "hay-kot/mealie"

# Icons
ICONS = {
    "breakfast": "mdi:egg-fried",
    "lunch": "mdi:bread-slice",
    "dinner": "mdi:pot-steam",
    "side": "mdi:bowl-mix-outline",
}

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
CAMERA = "camera"
UPDATE = "update"
PLATFORMS = [SENSOR]

# Defaults
DEFAULT_NAME = DOMAIN

CONF_EXTENDED = "extended"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
