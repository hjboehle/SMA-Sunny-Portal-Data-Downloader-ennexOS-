"""module downloader.main"""

from datetime import datetime, time
from zoneinfo import ZoneInfo
import sys
from downloader.logger_config import get_logger
from downloader.config import (
    SUNNY_PORTAL_API_DATA,
    SMA_DEVICE_DATA,
    TIME_ZONE,
)
from downloader.service.sunny_portal import fetch_data
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

    # Configure the date for which data should be downloaded
    download_day = datetime(2026, 1, 31).date()

    # Define time zones for Berlin and UTC
    tz = ZoneInfo(TIME_ZONE)
    utc_tz = ZoneInfo("UTC")

    # Start- and end times for the data fetch, converted to UTC
    start_date = datetime.combine(download_day, time(0, 0, 0), tzinfo=tz).astimezone(utc_tz)
    end_date = datetime.combine(download_day, time(23, 59, 59), tzinfo=tz).astimezone(utc_tz)

    fetch_data_result = fetch_data(
        SUNNY_PORTAL_API_DATA,
        SMA_DEVICE_DATA,
        start_date=start_date,
        end_date=end_date,
    )

    # Check if we have any data, even if some requests failed (valid=False)
    if not fetch_data_result["valid"] and not fetch_data_result.get("data"):
        logger.error("Downloader could not fetch data from Sunny Portal API. Exiting.")
        sys.exit(1)

    # Save each channel data to a separate file
    for item in fetch_data_result.get("data", []):
        channel_id = item.get("channelId", "unknown_channel")
        file_name = f"output/{download_day}_{channel_id}.json"
        if not save_data_to_json_file(item, file_name):
            logger.error("Could not save data for channel %s", channel_id)


if __name__ == "__main__":
    main()
