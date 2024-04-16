import requests


class TwitchAPI:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.requests = 0
        self.token = self.get_oauth_token()

    def get_oauth_token(self) -> str:
        print("Getting OAuth token...")
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        self.requests += 1
        return response.json()["access_token"]

    def get_data(self, url: str, params: dict) -> dict:
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        self.requests += 1
        return response.json()
