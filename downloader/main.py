"""module downloader.main"""

import sys
from downloader.logger_config import get_logger
from downloader.config import (
    SUNNY_PORTAL_API_BASE_URL,
    SUNNY_PORTAL_AUTHORIZATION_TOKEN,
    SMA_COMPONENT_ID,
)
from downloader.service.sunny_portal import fetch_data


def main():
    """
    Starts the downloader application.

    Args:
        None

    Returns:
        None
    """
    logger = get_logger(__name__)
    logger.info("Downloader gestartet.")
    fetch_data_result = fetch_data(
        api_base_url=SUNNY_PORTAL_API_BASE_URL,
        endpoint=f"widgets/gauge/power?componentId={SMA_COMPONENT_ID}&type=PvProduction",
        authorization_token=SUNNY_PORTAL_AUTHORIZATION_TOKEN,
    )
    if not fetch_data_result["valid"]:
        logger.error("Downloader could not fetch data from Sunny Portal API. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
