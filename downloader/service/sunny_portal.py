"""module downloader.service.sunny_portal"""

import time
from datetime import datetime
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
        "Authorization": f"Bearer {authorization_token.strip()}",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Origin": "https://ennexos.sunnyportal.com",
        "Connection": "keep-alive",
        "Referer": "https://ennexos.sunnyportal.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
    }


def _get_new_token(api_data: dict) -> str | None:
    """
    Attempts to fetch a new bearer token by simulating a login.

    THIS IS A PLACEHOLDER! You need to find the correct login endpoint and payload.
    1. Use browser dev tools on the login page to find the URL and payload.
    2. Update `login_url` and `login_payload`.
    3. Check the JSON response to find the key for the token (e.g., "access_token").
    """
    logger.info("Attempting to refresh authentication token...")

    # Wir nutzen den Standard OAuth2 Token-Endpunkt von SMA (Keycloak)
    # Basierend auf deiner URL: Realm = SMA, Client-ID = SPpbeOS
    login_url = "https://login.sma.energy/auth/realms/SMA/protocol/openid-connect/token"

    login_payload = {
        "grant_type": "password",
        "client_id": "SPpbeOS",  # Aus deiner URL extrahiert
        "username": api_data.get("username"),
        "password": api_data.get("password"),
        "scope": "openid",
    }

    if not all([login_payload["username"], login_payload["password"]]):
        logger.error("Username or password not configured. Cannot refresh token.")
        return None

    try:
        # OAuth2 erwartet Form-URL-Encoded Daten (data=...), kein JSON!
        # Header werden von requests automatisch gesetzt (Content-Type: application/x-www-form-urlencoded)
        response = requests.post(login_url, data=login_payload, timeout=10)

        if response.status_code == 200:
            token_data = response.json()
            new_token = token_data.get("access_token")
            if new_token:
                logger.info("Successfully refreshed authentication token.")
                return new_token
            logger.error("Login successful, but no token found in response: %s", token_data)
            return None

        logger.error(
            "Failed to refresh token. Login failed with status %s. URL: %s",
            response.status_code,
            login_url,
        )
        return None

    except requests.exceptions.RequestException as e:
        logger.error("An error occurred during token refresh: %s", e)
        return None


def fetch_data(
    api_data: dict,
    device_data: dict,
    start_date: datetime,
    end_date: datetime,
) -> dict:
    """
    Fetches data from the Sunny Portal API.

    Args:
        api_data (dict): The API data configuration.
        device_data (dict): The device data configuration.
        start_date (datetime): The start date for the data fetch.
        end_date (datetime): The end date for the data fetch.

    Returns:
        dict: The data fetched from the API.
    """
    logger.info("Data from Sunny Portal API are fetching...")
    fetch_data_result = {"valid": False}
    url = f"{api_data['api_base_url'].rstrip('/')}/{api_data['endpoint'].lstrip('/')}"
    headers = get_sunny_portal_header(api_data["authorization_token"])

    aggregated_data = []
    all_requests_valid = True

    for channel_id in device_data["channel_ids"]:
        # Create a simple payload with a single query item
        payload = {
            "queryItems": [
                {
                    "componentId": device_data["component_id"],
                    "channelId": channel_id,
                    "resolution": device_data.get("resolution", "FifteenMinutes"),
                    "timezone": "Europe/Berlin",
                    "aggregate": "Avg",
                    "multiAggregate": "Sum",
                    "allowDataReduction": True,
                }
            ],
            "dateTimeBegin": start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "dateTimeEnd": end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        }

        try:
            logger.debug("Fetching data for channel: %s", channel_id)
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            # Handle expired token (401 Unauthorized) and retry once.
            if response.status_code == 401:
                logger.warning(
                    "Received 401 Unauthorized. Token may have expired. Attempting refresh..."
                )
                new_token = _get_new_token(api_data)
                if new_token:
                    api_data["authorization_token"] = new_token
                    headers = get_sunny_portal_header(new_token)
                    logger.info("Retrying request for channel %s with new token.", channel_id)
                    response = requests.post(url, headers=headers, json=payload, timeout=10)
                else:
                    logger.error("Token refresh failed. Cannot continue for other channels.")
                    all_requests_valid = False
                    break  # Stop trying other channels if we can't log in

            if response.status_code == 200:
                # The API returns a list of results (even for one item).
                # We extend our aggregated list with these results.
                data = response.json()
                aggregated_data.extend(data)
            else:
                logger.error(
                    "Failed to fetch channel %s. Status: %s. Response: %s",
                    channel_id,
                    response.status_code,
                    response.text
                )
                all_requests_valid = False

            # Pause for 1 second to avoid stressing the API
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            logger.error("RequestException for channel %s: %s", channel_id, e)
            all_requests_valid = False

    if aggregated_data:
        fetch_data_result["valid"] = (
            all_requests_valid  # True only if ALL succeeded, or consider partial success
        )
        fetch_data_result["data"] = aggregated_data
        logger.info("Finished fetching. Got data for %s channels.", len(aggregated_data))

    return fetch_data_result
