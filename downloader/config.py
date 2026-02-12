"""module downloader.config"""

import os
from downloader.logger_config import get_logger

logger = get_logger(__name__)

SUNNY_PORTAL_API_BASE_URL = os.getenv("SUNNY_PORTAL_API_BASE_URL")
SUNNY_PORTAL_AUTHORIZATION_TOKEN = os.getenv("SUNNY_PORTAL_AUTHORIZATION_TOKEN")
SMA_COMPONENT_ID = os.getenv("SMA_COMPONENT_ID")
