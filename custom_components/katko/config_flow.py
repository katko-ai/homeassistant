"""Config flow for Katko.ai Infrastructure Radar integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
import homeassistant.helpers.config_validation as cv

from .const import CONF_API_KEY, CONF_LOCATION_NAME, CONF_RADIUS, DEFAULT_NAME, DEFAULT_RADIUS, DOMAIN

_LOGGER = logging.getLogger(__name__)

class KatkoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Katko.ai."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            location_name = user_input.get(CONF_LOCATION_NAME, DEFAULT_NAME)
            await self.async_set_unique_id(f"katko_{user_input[CONF_LATITUDE]}_{user_input[CONF_LONGITUDE]}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Katko ({location_name})",
                data=user_input,
            )

        # Default to Home Assistant instance latitude and longitude
        default_lat = self.hass.config.latitude
        default_lon = self.hass.config.longitude

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_LOCATION_NAME, default="Koti"): str,
                vol.Optional(CONF_LATITUDE, default=default_lat): cv.latitude,
                vol.Optional(CONF_LONGITUDE, default=default_lon): cv.longitude,
                vol.Optional(CONF_RADIUS, default=DEFAULT_RADIUS): vol.Coerce(float),
                vol.Optional(CONF_API_KEY, default=""): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
