"""module downloader.config"""

import os
import sys
import getpass
from downloader.logger_config import get_logger

logger = get_logger(__name__)

# The login URL is static for the SMA API, so we can provide a default.
SUNNY_PORTAL_API_LOGIN_URL = os.getenv("SUNNY_PORTAL_API_LOGIN_URL")
SUNNY_PORTAL_API_CLIENT_ID = "SPpbeOS"
SUNNY_PORTAL_API_BASE_URL = os.getenv("SUNNY_PORTAL_API_BASE_URL")
SUNNY_PORTAL_API_ENDPOINT = os.getenv("SUNNY_PORTAL_API_ENDPOINT")
SUNNY_PORTAL_USERNAME = os.getenv("SUNNY_PORTAL_USERNAME")
SUNNY_PORTAL_PASSWORD = os.getenv("SUNNY_PORTAL_PASSWORD")
SMA_COMPONENT_ID = os.getenv("SMA_COMPONENT_ID")

TIME_ZONE = os.getenv("TIME_ZONE")

# Validate that essential environment variables are set
REQUIRED_ENV_VARS = {
    "SUNNY_PORTAL_API_BASE_URL": SUNNY_PORTAL_API_BASE_URL,
    "SUNNY_PORTAL_API_ENDPOINT": SUNNY_PORTAL_API_ENDPOINT,
    "SMA_COMPONENT_ID": SMA_COMPONENT_ID,
    "TIME_ZONE": TIME_ZONE,
}

missing_vars = [key for key, value in REQUIRED_ENV_VARS.items() if not value]
if missing_vars:
    logger.error(
        "The following required environment variables are not set: %s",
        ", ".join(missing_vars),
    )
    sys.exit(1)

# Prompt for username if not set
if not SUNNY_PORTAL_USERNAME:
    logger.info("Username not found in environment variables. Requesting user input...")
    SUNNY_PORTAL_USERNAME = input("Please enter your Sunny Portal username: ")

# Prompt for password if not set
if not SUNNY_PORTAL_PASSWORD:
    logger.info("Password not found in environment variables. Requesting user input...")
    SUNNY_PORTAL_PASSWORD = getpass.getpass("Please enter your Sunny Portal password: ")

SUNNY_PORTAL_API_DATA = {
    "start_date": os.getenv("START_DATE"),
    "end_date": os.getenv("END_DATE"),
    "api_login_url": SUNNY_PORTAL_API_LOGIN_URL,
    "api_client_id": SUNNY_PORTAL_API_CLIENT_ID,
    "api_base_url": SUNNY_PORTAL_API_BASE_URL,
    "endpoint": SUNNY_PORTAL_API_ENDPOINT,
    "username": SUNNY_PORTAL_USERNAME,
    "password": SUNNY_PORTAL_PASSWORD,
}

"""
This dictionary SMA_DEVICE_DATA contains the configuration for the SMA device data to be
fetched from the Sunny Portal API. It includes:

- component_id: The ID of the component (inverter) to query data from.
- resolution: The time resolution for the data
    (e.g., "FiveMinutes", "FifteenMinutes", "OneHour", OneDay, OneMonth).
- channel_ids: A list of channel IDs to fetch.
    - Measurement.GridMs.TotW.Pv: AC Power from PV (Wechselrichter-Erzeugung AC)
    - Measurement.SpecificPower.Pv: Specific power (W/kWp)
    - Measurement.DcMs.Watt[0/1]: DC Power per String
    - Measurement.DcMs.Vol[0/1]: DC Voltage per String
    - Measurement.DcMs.Amp[0/1]: DC Current per String
    - Measurement.Metering.GridMs.TotWIn.Bat: Battery Charge Power
    - Measurement.Metering.GridMs.TotWOut.Bat: Battery Discharge Power
    - Measurement.Bat.ChaStt: Battery State of Charge (SoC)
    - Measurement.Bat.Diag.ActlCapacNom: Battery actual nominal capacity (Diagnosis)
    - Measurement.Metering.PCCMs.PlntW: Power at Grid Connection Point (Netzanschlusspunkt)
        (positive = feed-in, negative = grid-draw)
    - Measurement.Metering.PCCMs.PlntCsmpW: Total Power Consumption of the household (Hausverbrauch)
    - Measurement.GridMs.TotW: Total AC power of the inverter
    - Measurement.GridMs.Hz: Grid Frequency
    - Measurement.GridMs.PhV.phsA/B/C: Grid Voltage per Phase
    - Measurement.GridMs.A.phsA/B/C: Grid Current per Phase
"""


SMA_DEVICE_DATA = {
    "component_id": SMA_COMPONENT_ID,
    "resolution": os.getenv("SMA_RESOLUTION", "FiveMinutes"),
    "channel_ids": [
        # --- PV Generation ---
        "Measurement.GridMs.TotW.Pv",
        "Measurement.SpecificPower.Pv",
        # --- DC Side (Strings) ---
        "Measurement.DcMs.Watt[0]",
        "Measurement.DcMs.Watt[1]",
        "Measurement.DcMs.Vol[0]",
        "Measurement.DcMs.Vol[1]",
        "Measurement.DcMs.Amp[0]",
        "Measurement.DcMs.Amp[1]",
        # --- Battery ---
        "Measurement.Metering.GridMs.TotWIn.Bat",
        "Measurement.Metering.GridMs.TotWOut.Bat",
        "Measurement.Bat.ChaStt",
        "Measurement.Bat.Diag.ActlCapacNom",
        # --- Grid / PCC (Point of Common Coupling) ---
        "Measurement.Metering.PCCMs.PlntW",
        "Measurement.Metering.PCCMs.PlntCsmpW",
        # --- Grid Measurements (Inverter) ---
        "Measurement.GridMs.TotW",
        "Measurement.GridMs.Hz",
        "Measurement.GridMs.PhV.phsA",
        "Measurement.GridMs.PhV.phsB",
        "Measurement.GridMs.PhV.phsC",
        "Measurement.GridMs.A.phsA",
        "Measurement.GridMs.A.phsB",
        "Measurement.GridMs.A.phsC",
    ]
}
