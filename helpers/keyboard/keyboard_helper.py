import requests


class KeybboardHelper:

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    @property
    def base_url(self) -> str:
        return f"{self._host}:{self._port}"

    def press_key(self, key: str, duration_seconds: float = 0) -> dict:
        url = f"{self.base_url}/press"
        payload = {"key": key, "duration_seconds": duration_seconds}
        response = requests.post(url, json=payload)
        return response.json()

    def release_key(self, key: str) -> dict:
        url = f"{self.base_url}/release"
        payload = {"key": key}
        response = requests.post(url, json=payload)
        return response.json()

    def hold_key(self, key: str) -> dict:
        url = f"{self.base_url}/hold"
        payload = {"key": key}
        response = requests.post(url, json=payload)
        return response.json()
