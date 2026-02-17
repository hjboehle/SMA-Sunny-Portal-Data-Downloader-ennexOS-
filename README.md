# SMA Sunny Portal Data Downloader (ennexOS)

This project enables downloading all data visualized in the [SMA Sunny Portal](https://ennexos.sunnyportal.com).

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone [https://github.com/hjboehle/SMA-Sunny-Portal-Data-Downloader-ennexOS-.git](https://github.com/hjboehle/SMA-Sunny-Portal-Data-Downloader-ennexOS-.git)
cd SMA-Sunny-Portal-Data-Downloader-ennexOS-
```

## Preparation

The software provided here utilizes the same API as the Sunny Portal WebGUI. Therefore, the environment variable values must be retrieved from the browser's developer tools after you are logged in. In the "Network" tab, select a GET request. The request "headers" are displayed on the right. The required environment variables are defined as follows:

**Required:**

* `SUNNY_PORTAL_API_BASE_URL`: Composed of the protocol (https://) and the "Host".
* `SUNNY_PORTAL_AUTHORIZATION_TOKEN`: Found under Request Headers in the "Authorization" field (excluding the "Bearer " prefix).
* `SMA_COMPONENT_ID`: Can be found directly in the "headers".
* `SUNNY_PORTAL_LOGIN_URL`: The OAuth2 login endpoint URL.
* `SUNNY_PORTAL_API_ENDPOINT`: The API endpoint for data queries.
* `TIME_ZONE`: Your timezone (e.g., "Europe/Berlin").

**Optional (if not provided via environment variables):**

* `SUNNY_PORTAL_USERNAME`: Your Sunny Portal username. If not set, you will be prompted to enter it interactively.
* `SUNNY_PORTAL_PASSWORD`: Your Sunny Portal password. If not set, you will be prompted to enter it interactively (password input is hidden).

## Execution

To start the application, run the following command from the project's root directory:

```bash
python3 -m downloader.main
```
