"""The Katko.ai Infrastructure Radar integration."""
import async_timeout
from datetime import timedelta
import logging
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_API_KEY, CONF_RADIUS, DEFAULT_ENDPOINT, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Katko.ai from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = KatkoDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class KatkoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Katko.ai data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize."""
        self.entry = entry
        self.api_key = entry.data.get(CONF_API_KEY, "")
        self.latitude = entry.data.get(CONF_LATITUDE)
        self.longitude = entry.data.get(CONF_LONGITUDE)
        self.radius = entry.data.get(CONF_RADIUS, 20.0)

        # Default interval: 15 min (900s) for free, updated dynamically once tier info is fetched
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=900),
        )

    async def _async_update_data(self):
        """Fetch data from Katko.ai API."""
        params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "radius_km": self.radius,
            "api_key": self.api_key,
        }
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(DEFAULT_ENDPOINT, params=params, headers=headers) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error fetching Katko data: HTTP {response.status}")
                        data = await response.json()

                        # Dynamically adjust polling interval based on user tier
                        recommended_sec = data.get("tier_info", {}).get("recommended_interval_seconds", 900)
                        if self.update_interval != timedelta(seconds=recommended_sec):
                            _LOGGER.info("Updating Katko polling interval to %s seconds based on tier %s",
                                         recommended_sec, data.get("tier_info", {}).get("tier"))
                            self.update_interval = timedelta(seconds=recommended_sec)

                        return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Katko API: {err}") from err
