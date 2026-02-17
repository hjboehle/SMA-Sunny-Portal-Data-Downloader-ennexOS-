# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-02-14

### Added

- Automatic OAuth2 token refresh mechanism when the API returns a 401 Unauthorized status.
- Configuration for Sunny Portal username and password (`SUNNY_PORTAL_USERNAME`, `SUNNY_PORTAL_PASSWORD`).
- Comprehensive list of available measurement channels in `config.py` (PV, Battery, Grid, DC Strings).
- Automatic retry mechanism with up to 3 attempts for transient API failures (non-200 status codes, network errors).
- Configurable request timeout parameter in `fetch_data()` function (default: 10 seconds).
- Interactive prompts for username and password input if not provided via environment variables (password input is hidden).
- Validation for required environment variables (`SUNNY_PORTAL_API_BASE_URL`, `SMA_COMPONENT_ID`, etc.) on startup.
- Default value for `SUNNY_PORTAL_LOGIN_URL` to simplify configuration.

### Changed

- Refactored `fetch_data` service to query each channel individually instead of a bulk request.
- Changed default data resolution from "PT15M" to "FifteenMinutes" to match API requirements.
- Updated `main.py` to save output files individually per channel with a `YYYY-MM-DD_ChannelName.json` naming convention.
- Updated `save_data_to_json_file` utility to handle `dict` and `list` input types for automatic JSON serialization.
- Improved `fetch_data()` with retry logic: API rate limits and transient errors are automatically retried before aborting.
- Optimized polling behavior: API is paused for 1 second only after successful requests, not after failed attempts.
- Updated `main.py` to skip saving JSON files if the API returns empty values for a channel.
- Changed authentication flow to perform an initial login at application start instead of waiting for a 401 error.

### Fixed

- Fixed issue where `save_data_to_json_file` expected a string but received a dictionary.
- Fixed critical logic error in `_get_new_token()` where error logging was executed unconditionally, causing duplicate error messages.
- Fixed missing `login_url` validation in `_get_new_token()` to prevent crashes with incomplete configuration.
- Added proper exception handling for JSON parsing errors in `fetch_data()` to prevent crashes on malformed API responses.
- Fixed inconsistent timeout parameter usage in `fetch_data()` (was hardcoded to 10 seconds in first request, now uses configurable parameter everywhere).

## [0.0.1] - 2026-02-12

### Added [0.0.1]

- Initial release of the SMA Sunny Portal Data Downloader.
- Core service `sunny_portal.py` to fetch data from the API.
- Application entry point `main.py`.
- Configuration management via environment variables (`config.py`).
- Unit tests for the service layer (`tests/service/test_sunny_portal.py`).
- Code formatting configuration using `black` in `pyproject.toml`.
- Basic error handling for API timeouts, connection errors, and authentication failures.
- Logging configuration.
- Documentation on how to run the application in `README.md`.
