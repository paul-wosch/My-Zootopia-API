"""Fetch data from API Ninjas."""
import requests
from dotenv import dotenv_values

API_KEY = dotenv_values(".env").get("API_KEY", None)
BASE_URL = "https://api.api-ninjas.com/v1/"
HEADERS = {"X-Api-Key": API_KEY}
TIMEOUT = 4


def retrieve_data_from_api(endpoint, payload=None) -> requests.Response | None:
    """Return response from REST API for given endpoint and payload."""
    url = BASE_URL + endpoint
    try:
        return requests.get(url, headers=HEADERS, params=payload, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        print(f"Request to {url} timed out")
    return None


def get_animals(name: str) -> list[dict] | None:
    """Return up to 10 animals matching the given name.

    If no match is found the returned list will be empty.
    Return none if there is a miss-configured API key.
    """
    endpoint = "animals"
    payload = {"name": name}
    response = retrieve_data_from_api(endpoint, payload)
    if response:
        return response.json()
    return None


if __name__ == "__main__":
    pass
