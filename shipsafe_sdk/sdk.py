import requests

class ShipSafe:
    def __init__(self, api_key, project_id, base_url="http://127.0.0.1:5000"):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = base_url

    def is_flag_enabled(self, flag_name):
        url = f"{self.base_url}/api/projects/{self.project_id}/flags/{flag_name}"
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            response_data = response.json()
            raise ValueError(f"ShipSafe API error: {response_data.get('error', 'Unknown error')}") from error

        data = response.json()
        return data["enabled"] == 1

