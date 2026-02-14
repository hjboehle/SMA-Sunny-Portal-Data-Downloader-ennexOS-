"""module downloader.config"""

import os
from downloader.logger_config import get_logger

logger = get_logger(__name__)

SUNNY_PORTAL_API_BASE_URL = os.getenv("SUNNY_PORTAL_API_BASE_URL")
SUNNY_PORTAL_API_ENDPOINT = os.getenv("SUNNY_PORTAL_API_ENDPOINT")
SUNNY_PORTAL_AUTHORIZATION_TOKEN = os.getenv("SUNNY_PORTAL_AUTHORIZATION_TOKEN")
SUNNY_PORTAL_USERNAME = os.getenv("SUNNY_PORTAL_USERNAME")
SUNNY_PORTAL_PASSWORD = os.getenv("SUNNY_PORTAL_PASSWORD")
SMA_COMPONENT_ID = os.getenv("SMA_COMPONENT_ID")

TIME_ZONE = os.getenv("TIME_ZONE")

SUNNY_PORTAL_API_DATA = {
    "api_base_url": SUNNY_PORTAL_API_BASE_URL,
    "endpoint": SUNNY_PORTAL_API_ENDPOINT,
    "authorization_token": SUNNY_PORTAL_AUTHORIZATION_TOKEN,
    "username": SUNNY_PORTAL_USERNAME,
    "password": SUNNY_PORTAL_PASSWORD,
}

"""
Measurement channel configuration for the SMA Sunny Portal API.

This dictionary defines which data channels to query.

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
    "resolution": "FifteenMinutes",
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
