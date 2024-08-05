from datetime import timedelta
import logging

import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_UPDATE_INTERVAL
from homeassistant.core import HomeAssistant

from homeassistant.components.light import LightEntity
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .coordinator import RpiHomeCoordinator

from .const import (DOMAIN, UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

logger = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    # install some base data for ourselves
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    update_interval = entry.options.get(UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    logger.debug(f"Update interval: {update_interval}")
    for ar in entry.data:
        logger.debug(ar)

    # assuming API object stored here by async_setup?
    my_api = hass.data[DOMAIN][entry.entry_id]
    coordinator = RpiHomeCoordinator(hass, my_api)

    # Fetch initial data so we have data when entities subscribe
    #
    # If the refresh fails, async_config_entry_first_refresh will
    # raise ConfigEntryNotReady and setup will try again later
    #
    # If you do not want to retry setup on failure, use
    # coordinator.async_refresh() instead
    #
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        MyEntity(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )
