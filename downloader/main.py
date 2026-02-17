"""module downloader.main"""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
import sys
from downloader.logger_config import get_logger
from downloader.config import (
    SUNNY_PORTAL_API_DATA,
    SMA_DEVICE_DATA,
    TIME_ZONE,
)
from downloader.service.sunny_portal import fetch_data, get_new_token
from downloader.utils.file import save_data_to_json_file


def main():
    """
    Starts the downloader application.

    Args:
        None

    Returns:
        None
    """
    logger = get_logger(__name__)
    logger.info("Starting the downloader application.")

    # Get authentication token by logging in
    auth_token = get_new_token(SUNNY_PORTAL_API_DATA)
    if not auth_token:
        logger.error("Failed to get authentication token. Exiting.")
        sys.exit(1)

    # Add the obtained token to our API configuration for subsequent requests
    SUNNY_PORTAL_API_DATA["authorization_token"] = auth_token

    # Configure the date for which data should be downloaded
    start_date_str = SUNNY_PORTAL_API_DATA.get("start_date")
    end_date_str = SUNNY_PORTAL_API_DATA.get("end_date")

    if not start_date_str or not end_date_str:
        logger.error("Start date or end date not found in environment variables. Exiting.")
        sys.exit(1)

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    current_date = start_date
    while current_date <= end_date:
        # Define time zone and UTC
        tz = ZoneInfo(TIME_ZONE)
        utc_tz = ZoneInfo("UTC")

        # Start- and end times for the data fetch, converted to UTC
        start_datetime = datetime.combine(current_date, time(0, 0, 0), tzinfo=tz).astimezone(utc_tz)
        end_datetime = datetime.combine(current_date, time(23, 59, 59), tzinfo=tz).astimezone(
            utc_tz
        )

        fetch_data_result = fetch_data(
            SUNNY_PORTAL_API_DATA,
            SMA_DEVICE_DATA,
            start_date=start_datetime,
            end_date=end_datetime,
        )

        # Save each channel data to a separate file
        for item in fetch_data_result.get("data", []):
            channel_id = item.get("channelId", "unknown_channel")

            if not item.get("values"):
                logger.info("No values for channel %s on %s. Skipping save.", channel_id, current_date)
                continue

            file_name = f"output/{current_date}_{channel_id}.json"
            if not save_data_to_json_file(item, file_name):
                logger.error("Could not save data for channel %s", channel_id)
        current_date += timedelta(days=1)


if __name__ == "__main__":
    main()
