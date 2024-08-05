import logging
import voluptuous as vol

from typing import Any

from homeassistant import exceptions
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, CONN_CLASS_LOCAL_POLL
from homeassistant.components.zeroconf import ZeroconfServiceInfo
from homeassistant.const import CONF_NAME, CONF_HOST, CONF_ROOM
from homeassistant.helpers.area_registry import AreaRegistry

from rpi_home import SERIAL_NUMBER
from .const import DOMAIN, DISCOVERED_DEVICES, UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL

logger = logging.getLogger(__name__)

CONFIGURED = "configured"

class RpiHomeConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_LOCAL_POLL

    async def _build_from_data(self, data: dict[str, Any]) -> ConfigFlowResult:
        pass

    async def async_step_user(self, data: dict[str, Any] | None = None):
        # start with no errrors
        errors = {}

        # if the input came from a form that got filled in...
        if data is not None:
            try:
                # do the configuration
                return await self._build_from_data(data)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception as exc:  # pylint: disable=broad-except
                logger.exception(f"Unexpected exception {exc}")
                errors["base"] = "unknown"

        # get the list of areas
        area_registry = AreaRegistry(self.hass)
        await area_registry.async_load()
        areas = area_registry.async_list_areas()
        area_names = [area.name for area in areas]

        # look to see if zeroconf found a device already and prefill the ip address if it did
        devices: dict[str, ZeroconfServiceInfo] = self.hass.data.setdefault(DISCOVERED_DEVICES, {})
        unconfigured_device = next(((key, device) for key, device in devices.items() if not device.properties.get(CONFIGURED, False)), None)
        (device_name, device_host, device_room, update_interval) = (None, None, None, DEFAULT_UPDATE_INTERVAL)
        if unconfigured_device is not None:
            device_name = unconfigured_device[1].name
            device_host = unconfigured_device[1].hostname
            logger.debug(f"in user setup with unconfigured device: {device_name} ({device_host})")

            # look to see if the name starts with any of the device_areas, or vice versa, e.g.
            # "Bedroom 3-in-1 Sensor"
            for area_name in area_names:
                if device_name.startswith(area_name):
                    device_room = area_name
                    logger.debug(f"  ...in room: {device_room}")

        # get approval from the user
        data_schema = vol.Schema({
            vol.Required(CONF_NAME, default=device_name): str,
            vol.Required(CONF_HOST, default=device_host): str,
            vol.Required(CONF_ROOM, default=device_room): str,
            vol.Required(UPDATE_INTERVAL, default=update_interval): str
        })
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo):
        # our zero conf:
        # name (X2)
        # address: 10.0.62.91
        # host: rpi-home-x2
        # properties: {rpi_home: 2.1.5, serial_number: 849af7d8581340a0}
        logger.debug(f"zeroconf discovered (device: {discovery_info.name}, hostname: {discovery_info.hostname}, ip_address: {discovery_info.ip_address})")

        # use the serial number as a unique identifier
        existing_entry = await self.async_set_unique_id(discovery_info.properties[SERIAL_NUMBER])
        self._abort_if_unique_id_configured()

        # report that we got this far - the device is unique
        logger.debug(f"unique device with serial number: {discovery_info.properties[SERIAL_NUMBER]})")

        # we store the discovered device so the user config flow can get it
        devices: dict[str, ZeroconfServiceInfo] = self.hass.data.setdefault(DISCOVERED_DEVICES, {})
        devices[discovery_info.name] = discovery_info

        # wait for the user to configure it
        return await self.async_step_user()


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
