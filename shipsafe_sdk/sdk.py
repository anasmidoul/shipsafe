import requests

class ShipSafe:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id

    def is_flag_enabled(self, flag_name):
        url = f"http://127.0.0.1:5000/api/projects/{self.project_id}/flags/{flag_name}"
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            response_data = response.json() 
            raise ValueError(f"ShipSafe API error: {response_data['error']}") from error
        data = response.json()
        return data["enabled"] == 1
    
