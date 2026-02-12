# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-02-12

### Added

- Initial release of the SMA Sunny Portal Data Downloader.
- Core service `sunny_portal.py` to fetch data from the API.
- Application entry point `main.py`.
- Configuration management via environment variables (`config.py`).
- Unit tests for the service layer (`tests/service/test_sunny_portal.py`).
- Code formatting configuration using `black` in `pyproject.toml`.
- Basic error handling for API timeouts, connection errors, and authentication failures.
- Logging configuration.
- Documentation on how to run the application in `README.md`.
