import requests
import json
import random
import string
import time


class UserNotSupportedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args, "User cannot be empty or is invalid!")


def randomCode():
    rd_string = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(21)])
    return rd_string


class GithubInfo:
    def __init__(self, username: str) -> None:
        if not username or username == "":
            raise UserNotSupportedError
        self.username = username
        with open("config.auth.json", "r", encoding="utf-8") as file:
            self.api_secrets = json.loads(file.read())

        self.api_base_url = f"https://api.github.com/users/{username}/repos"

    def processResponse(self, response: list) -> list:
        new_response = []
        for item in response:
            if item['description'] is None:
                item['description'] = ""
            new_response.append({
                "name": item['name'], 
                'full_name': item['full_name'], 
                "url": item["html_url"],
                "description": item['description'],
                })
        return new_response

    def hasLimitLeft(self) -> dict:
        has_limit = False
        header = {
            "Authorization": f"token {self.api_secrets['kamutoken']}"
            }
        response = requests.get(f"https://api.github.com/rate_limit", headers=header)
        if response.status_code == 200:
            response = response.json()
            if response['resources']['core']['remaining'] > 0:
                has_limit = True
            reset_time = response['resources']['core']['reset'] - int(time.time()) 
            return {"reset": reset_time, "has_limit": has_limit}
        return {"has_limit": False, "reset": -1}
    
    def makeRequest(self) -> list:
        header = {
            "Authorization": f"token {self.api_secrets['kamutoken']}"
            }
        has_limit = self.hasLimitLeft()
        if has_limit['has_limit']:
            response = requests.get(self.api_base_url, headers=header)
        print("Rate limit resets in", has_limit['reset'])
        if response.status_code == 200:
            return self.processResponse(response.json())
        print(response.content)
        raise UserNotSupportedError


if __name__ == "__main__":
    github = GithubInfo("kamuridesu")
    (github.makeRequest())
