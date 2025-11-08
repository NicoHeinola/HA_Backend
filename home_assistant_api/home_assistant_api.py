class HomeAssistantAPI:
    """Home Assistant API integration base class"""

    def __init__(self, ha_url: str, access_token: str) -> None:
        self._ha_url: str = ha_url
        self._access_token: str = access_token

    @property
    def _authorization_header(self) -> dict:
        """Return authorization header for requests."""
        return {"Authorization": f"Bearer {self._access_token}"}
