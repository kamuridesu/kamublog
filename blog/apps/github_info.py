import requests


class UserNotSupportedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args, "User cannot be empty or is invalid!")


class GithubInfo:
    def __init__(self, username: str) -> None:
        if not username or username == "":
            raise UserNotSupportedError
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
    
    def makeRequest(self) -> list:
        response = requests.get(self.api_base_url)
        if response.status_code == 200:
            return self.processResponse(response.json())
        raise UserNotSupportedError


if __name__ == "__main__":
    github = GithubInfo("")
    github.makeRequest()