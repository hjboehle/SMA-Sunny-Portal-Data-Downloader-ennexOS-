# SMA Sunny Portal Data Downloader (ennexOS)

This project enables downloading all data visualized in the [SMA Sunny Portal](https://ennexos.sunnyportal.com).

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone [https://github.com/hjboehle/SMA-Sunny-Portal-Data-Downloader-ennexOS-.git](https://github.com/hjboehle/SMA-Sunny-Portal-Data-Downloader-ennexOS-.git)
cd SMA-Sunny-Portal-Data-Downloader-ennexOS-
```

## Preparation

The software requires several environment variables to be set. For authentication, you need to provide your username and password (`SUNNY_PORTAL_USERNAME`, `SUNNY_PORTAL_PASSWORD`).

Other required values can be retrieved from your browser's developer tools while you are logged into the Sunny Portal. Open the "Network" tab, trigger an API request (e.g., by viewing details), and inspect the request.

The following variables must be set:

* `SUNNY_PORTAL_API_BASE_URL`: The base URL for the API. Typically [https://uiapi.sunnyportal.com/api/v1](https://uiapi.sunnyportal.com/api/v1).
* `SUNNY_PORTAL_API_ENDPOINT`: The endpoint for fetching data. Typically `plant-data`.
* `SMA_COMPONENT_ID`: The unique ID of your inverter. This can be found in the "Payload" or "Body" of an API request as `componentId`.
* `TIME_ZONE`: Your local timezone, e.g., `Europe/Berlin`.
* `SUNNY_PORTAL_LOGIN_URL`: The URL for authentication. This has a default value [https://login.sma.energy/auth/realms/SMA/protocol/openid-connect/token](https://login.sma.energy/auth/realms/SMA/protocol/openid-connect/token) and usually does not need to be set manually.
* `START_DATE`: The start date for the data download in `YYYY-MM-DD` format (e.g., `2025-01-01`).
* `END_DATE`: The end date for the data download in `YYYY-MM-DD` format (e.g., `2025-01-31`).
* `SMA_RESOLUTION`: (Optional) The time resolution for the data. Defaults to `FiveMinutes`. Other possible values are `FifteenMinutes`, `OneHour`, `OneDay`.

## Execution

To start the application, run the following command from the project's root directory:

```bash
python3 -m downloader.main
```
