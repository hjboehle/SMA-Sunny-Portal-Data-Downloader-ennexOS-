"""module downloader.service.sunny_portal"""

import json
import requests
from downloader.logger_config import get_logger

logger = get_logger(__name__)


def get_sunny_portal_header(authorization_token: str) -> dict:
    """
    Generates the header for accessing the Sunny Portal API.

    Args:
        authorization_token (str): The authorization token for accessing the API.

    Returns:
        dict: The header for accessing the API.
    """
    return {
        "Authorization": f"Bearer {authorization_token}",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "de,en-US;q=0.9,en;q=0.8",
        "Origin": "https://ennexos.sunnyportal.com",
        "Connection": "keep-alive",
        "Referer": "https://ennexos.sunnyportal.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }


def fetch_data(api_base_url: str, endpoint: str, authorization_token: str) -> dict:
    """
    Fetches data from the Sunny Portal API.

    Args:
        endpoint (str): The endpoint of the Sunny Portal API (e.g. 'dashboards').
        authorization_token (str): The authorization token for accessing the API.

    Returns:
        dict: The data fetched from the API.
    """
    logger.info("Data from Sunny Portal API are fetching...")
    fetch_data_result = {"valid": False}
    url = f"{api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = get_sunny_portal_header(authorization_token)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            fetch_data_result["valid"] = True
            fetch_data_result["data"] = response.json()
            logger.info(
                "Data from Sunny Portal API fetched successfully:\n%s",
                json.dumps(fetch_data_result["data"], indent=4),
            )
        else:
            logger.error(
                "Failed to fetch data from Sunny Portal API. Status code: %s", response.status_code
            )
    except requests.exceptions.Timeout as e:
        logger.error("Timeout while fetching data from Sunny Portal API: %s", e)
    except requests.exceptions.ConnectionError as e:
        logger.error("Connection error while fetching data from Sunny Portal API: %s", e)
    except requests.exceptions.TooManyRedirects as e:
        logger.error("Too many redirects while fetching data from Sunny Portal API: %s", e)
    except requests.exceptions.RequestException as e:
        logger.error("An error occurred while fetching data from Sunny Portal API: %s", e)
    return fetch_data_result
