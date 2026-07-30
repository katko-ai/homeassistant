"""Constants for the Katko.ai Infrastructure Radar integration."""

DOMAIN = "katko"

DEFAULT_NAME = "Katko.ai Infratutka"
DEFAULT_RADIUS = 20.0  # km
DEFAULT_INTERVAL_COMMUNITY = 900  # 15 minutes for Community tier
DEFAULT_INTERVAL_PLUS = 60  # 1 minute for Plus/Pro tier

CONF_API_KEY = "api_key"
CONF_RADIUS = "radius"
CONF_LOCATION_NAME = "location_name"

DEFAULT_ENDPOINT = "https://europe-west1-katko-dev-e5c3a.cloudfunctions.net/serve_api_ha_check"
