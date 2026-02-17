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
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/144.0.0.0 Safari/537.36",
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


def _get_new_token(api_data: dict) -> dict:
    """
    Attempts to fetch a new bearer token by simulating a login.

    Args:
        api_data (dict): The API data configuration containing api_login_url,
                        api_client_id, username, and password.

    Returns:
        dict: A dictionary with "valid" (bool) and "new_token" (str) keys if
              successful, otherwise {"valid": False}.
    """
    logger.info("Attempting to refresh authentication token...")

    # Validate required configuration
    login_url = api_data.get("api_login_url")
    username = api_data.get("username")
    password = api_data.get("password")

    if not login_url:
        logger.error("Login URL not configured. Cannot refresh token.")
        return {"valid": False}

    if not all([username, password]):
        logger.error("Username or password not configured. Cannot refresh token.")
        return {"valid": False}

    login_payload = {
        "grant_type": "password",
        "client_id": api_data.get("api_client_id"),
        "username": username,
        "password": password,
        "scope": "openid",
    }

    try:
        response = requests.post(login_url, data=login_payload, timeout=10)

        if response.status_code == 200:
            try:
                token_data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error("Failed to parse token response JSON: %s", e)
                return {"valid": False}

            new_token = token_data.get("access_token")
            if new_token:
                logger.info("Successfully refreshed authentication token.")
                return {"valid": True, "new_token": new_token}

            logger.error("Login successful, but no token found in response: %s", token_data)
            return {"valid": False}

        logger.error(
            "Failed to refresh token. Login failed with status %s. URL: %s",
            response.status_code,
            login_url,
        )
        return {"valid": False}

    except requests.exceptions.RequestException as e:
        logger.error("An error occurred during token refresh: %s", e)
        return {"valid": False}


def fetch_data(
    api_data: dict,
    device_data: dict,
    start_date: datetime,
    end_date: datetime,
    timeout: int = 10,
) -> dict:
    """
    Fetches data from the Sunny Portal API.

    Args:
        api_data (dict): The API data configuration containing api_base_url,
            endpoint, and authorization_token.
        device_data (dict): The device data configuration containing channel_ids
            and component_id.
        start_date (datetime): The start date for the data fetch.
        end_date (datetime): The end date for the data fetch.
        timeout (int): Request timeout in seconds. Defaults to 10.

    Returns:
        dict: Dictionary with "valid" (bool) and optional "data" (list) keys.
            {"valid": False} if no data fetched or errors occurred,
            {"valid": True, "data": [...]} on success.
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

        max_retries = 3
        retry_count = 0
        channel_success = False

        while retry_count < max_retries and not channel_success:
            try:
                logger.debug(
                    "Fetching data for channel: %s (attempt %d/%d)",
                    channel_id,
                    retry_count + 1,
                    max_retries,
                )
                response = requests.post(url, headers=headers, json=payload, timeout=timeout)

                # Handle expired token (401 Unauthorized) and retry once.
                if response.status_code == 401:
                    logger.warning(
                        "Received 401 Unauthorized. Token may have expired. Attempting refresh..."
                    )
                    new_token = _get_new_token(api_data)
                    if new_token["valid"]:
                        api_data["authorization_token"] = new_token["new_token"]
                        headers = get_sunny_portal_header(new_token["new_token"])
                        logger.info("Retrying request for channel %s with new token.", channel_id)
                        response = requests.post(
                            url, headers=headers, json=payload, timeout=timeout
                        )
                    else:
                        logger.error("Token refresh failed. Cannot continue for other channels.")
                        all_requests_valid = False
                        break

                if response.status_code == 200:
                    # The API returns a list of results (even for one item).
                    # We extend our aggregated list with these results.
                    try:
                        data = response.json()
                        aggregated_data.extend(data)
                        channel_success = True
                        # Pause for 1 second to avoid stressing the API
                        time.sleep(1)
                    except requests.exceptions.JSONDecodeError as e:
                        logger.error(
                            "Failed to parse JSON response for channel %s: %s",
                            channel_id,
                            e,
                        )
                        all_requests_valid = False
                        break
                else:
                    retry_count += 1
                    if retry_count < max_retries:
                        logger.warning(
                            "Failed to fetch channel %s. Status: %s. Retrying... (%d/%d)",
                            channel_id,
                            response.status_code,
                            retry_count,
                            max_retries,
                        )
                        time.sleep(1)
                    else:
                        logger.error(
                            "Failed to fetch channel %s after %d attempts. Status: %s. "
                            "Response: %s",
                            channel_id,
                            max_retries,
                            response.status_code,
                            response.text,
                        )
                        all_requests_valid = False
                        break

            except requests.exceptions.RequestException as e:
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(
                        "RequestException for channel %s: %s. Retrying... (%d/%d)",
                        channel_id,
                        e,
                        retry_count,
                        max_retries,
                    )
                    time.sleep(1)
                else:
                    logger.error(
                        "RequestException for channel %s after %d attempts: %s",
                        channel_id,
                        max_retries,
                        e,
                    )
                    all_requests_valid = False
                    break

        # If all retries failed, abort
        if not channel_success and all_requests_valid is False:
            break

    if aggregated_data:
        fetch_data_result["valid"] = (
            all_requests_valid  # True only if ALL succeeded, or consider partial success
        )
        fetch_data_result["data"] = aggregated_data
        logger.info("Finished fetching. Got data for %s channels.", len(aggregated_data))

    return fetch_data_result
