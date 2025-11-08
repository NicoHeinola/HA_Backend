import logging
import requests
from home_assistant_api.home_assistant_api import HomeAssistantAPI

logger = logging.getLogger(__name__)


class HAWizLightAPI(HomeAssistantAPI):
    """Home Assistant Wiz Lights integration"""

    def __init__(self, ha_url: str, access_token: str):
        super().__init__(ha_url, access_token)

    def turn_off(self, entity_id: str) -> bool:
        """Turn off a Wiz light."""
        response: requests.Response = self._call_service("light", "turn_off", {"entity_id": f"light.{entity_id}"})
        return response.status_code == 200

    def turn_on(self, entity_id: str) -> bool:
        """Turn on a Wiz light."""
        response: requests.Response = self._call_service("light", "turn_on", {"entity_id": f"light.{entity_id}"})
        return response.status_code == 200

    def toggle(self, entity_id: str) -> bool:
        """Toggle a Wiz light."""
        light_state: dict = self.get_light_state(entity_id)
        print("STATE RESPONSE", light_state)
        return True

    def set_rgb_color(self, entity_id: str, r: int, g: int, b: int) -> bool:
        """Set the RGB color of a Wiz light."""
        payload = {"entity_id": f"light.{entity_id}", "rgb_color": [r, g, b]}
        response: requests.Response = self._call_service("light", "turn_on", payload)
        return response.status_code == 200

    def set_brightness(self, entity_id: str, brightness: int) -> bool:
        """Set the brightness of a Wiz light."""
        payload = {"entity_id": f"light.{entity_id}", "brightness": brightness}
        response: requests.Response = self._call_service("light", "turn_on", payload)
        return response.status_code == 200

    def get_light_state(self, entity_id: str) -> dict:
        """Get the current state of a Wiz light."""
        headers = self._authorization_header
        response = requests.get(f"{self._ha_url}/api/states/light.{entity_id}", headers=headers)

        response.raise_for_status()

        return response.json()
