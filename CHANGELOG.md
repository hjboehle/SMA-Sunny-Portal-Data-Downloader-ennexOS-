# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-02-14

### Added

- Automatic OAuth2 token refresh mechanism when the API returns a 401 Unauthorized status.
- Configuration for Sunny Portal username and password (`SUNNY_PORTAL_USERNAME`, `SUNNY_PORTAL_PASSWORD`).
- Comprehensive list of available measurement channels in `config.py` (PV, Battery, Grid, DC Strings).

### Changed

- Refactored `fetch_data` service to query each channel individually instead of a bulk request.
- Changed default data resolution from "PT15M" to "FifteenMinutes" to match API requirements.
- Updated `main.py` to save output files individually per channel with a `YYYY-MM-DD_ChannelName.json` naming convention.
- Updated `save_data_to_json_file` utility to handle `dict` and `list` input types for automatic JSON serialization.

### Fixed

- Fixed issue where `save_data_to_json_file` expected a string but received a dictionary.

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
