"""Sensor platform for Katko.ai Infrastructure Radar integration."""
import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_LOCATION_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)

SEVERITY_ICONS = {
    "none": "mdi:shield-check",
    "minor": "mdi:alert-outline",
    "medium": "mdi:alert-rhombus-outline",
    "major": "mdi:alert-octagon",
    "critical": "mdi:lightning-bolt-alert",
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Katko.ai sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    location_name = entry.data.get(CONF_LOCATION_NAME, "Koti")

    entities = [
        KatkoActiveDisruptionsSensor(coordinator, entry, location_name),
        KatkoHighestSeveritySensor(coordinator, entry, location_name),
        KatkoTelecomOutagesSensor(coordinator, entry, location_name),
        KatkoElectricityOutagesSensor(coordinator, entry, location_name),
        KatkoUserTierSensor(coordinator, entry, location_name),
    ]

    async_add_entities(entities)

class KatkoBaseEntity(CoordinatorEntity, SensorEntity):
    """Base entity for Katko.ai sensors."""

    def __init__(self, coordinator, entry, location_name):
        """Initialize the base entity."""
        super().__init__(coordinator)
        self.entry = entry
        self.location_name = location_name

    @property
    def device_info(self):
        """Return device info to group all sensors under a single Katko Radar device."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": f"Katko.ai Infratutka ({self.location_name})",
            "manufacturer": "Katko.ai",
            "model": "Global Infrastructure Radar API",
            "sw_version": "1.0.0",
        }

class KatkoActiveDisruptionsSensor(KatkoBaseEntity):
    """Sensor for total active disruptions count."""

    def __init__(self, coordinator, entry, location_name):
        super().__init__(coordinator, entry, location_name)
        self._attr_name = f"Katko Aktiiviset Häiriöt ({location_name})"
        self._attr_unique_id = f"{entry.entry_id}_active_disruptions"
        self._attr_icon = "mdi:radar"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Return active disruptions count."""
        if not self.coordinator.data:
            return 0
        return self.coordinator.data.get("active_count", 0)

    @property
    def extra_state_attributes(self):
        """Return attributes including disruption list and radius."""
        if not self.coordinator.data:
            return {}
        return {
            "status": self.coordinator.data.get("status"),
            "radius_km": self.coordinator.data.get("radius_km"),
            "disruptions": self.coordinator.data.get("disruptions", []),
        }

class KatkoHighestSeveritySensor(KatkoBaseEntity):
    """Sensor for highest active disruption severity."""

    def __init__(self, coordinator, entry, location_name):
        super().__init__(coordinator, entry, location_name)
        self._attr_name = f"Katko Vakavin Häiriötaso ({location_name})"
        self._attr_unique_id = f"{entry.entry_id}_highest_severity"

    @property
    def native_value(self):
        """Return highest severity string."""
        if not self.coordinator.data:
            return "none"
        return self.coordinator.data.get("summary", {}).get("highest_severity", "none")

    @property
    def icon(self):
        """Return dynamic icon based on severity."""
        sev = self.native_value
        return SEVERITY_ICONS.get(sev, "mdi:shield-check")

class KatkoTelecomOutagesSensor(KatkoBaseEntity):
    """Sensor for active telecom outages."""

    def __init__(self, coordinator, entry, location_name):
        super().__init__(coordinator, entry, location_name)
        self._attr_name = f"Katko Telekatkot ({location_name})"
        self._attr_unique_id = f"{entry.entry_id}_telecom_outages"
        self._attr_icon = "mdi:cellphone-tower-off"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        if not self.coordinator.data:
            return 0
        return self.coordinator.data.get("summary", {}).get("category_counts", {}).get("telecom", 0)

class KatkoElectricityOutagesSensor(KatkoBaseEntity):
    """Sensor for active electricity outages."""

    def __init__(self, coordinator, entry, location_name):
        super().__init__(coordinator, entry, location_name)
        self._attr_name = f"Katko Sähkökatkot ({location_name})"
        self._attr_unique_id = f"{entry.entry_id}_electricity_outages"
        self._attr_icon = "mdi:power-plug-off"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        if not self.coordinator.data:
            return 0
        return self.coordinator.data.get("summary", {}).get("category_counts", {}).get("electricity", 0)

class KatkoUserTierSensor(KatkoBaseEntity):
    """Diagnostic sensor for user's Katko subscription tier."""

    def __init__(self, coordinator, entry, location_name):
        super().__init__(coordinator, entry, location_name)
        self._attr_name = f"Katko Tilaustaso ({location_name})"
        self._attr_unique_id = f"{entry.entry_id}_user_tier"
        self._attr_icon = "mdi:star-crown-outline"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        if not self.coordinator.data:
            return "community"
        return self.coordinator.data.get("tier_info", {}).get("tier", "community")

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data:
            return {}
        return self.coordinator.data.get("tier_info", {})
