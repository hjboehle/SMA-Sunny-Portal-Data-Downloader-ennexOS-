"""module tests.service.sunny_portal"""

from unittest.mock import Mock, patch
import requests
from downloader.service.sunny_portal import fetch_data, get_sunny_portal_header


def test_get_sunny_portal_header():
    """Testet, ob die Header korrekt mit dem Token erstellt werden."""
    token = "mein_geheimes_token"
    headers = get_sunny_portal_header(token)

    assert headers["Authorization"] == "Bearer mein_geheimes_token"
    assert headers["Origin"] == "https://ennexos.sunnyportal.com"
    assert headers["Accept"] == "application/json, text/plain, */*"
    assert headers["Sec-Fetch-Site"] == "same-site"


@patch("downloader.service.sunny_portal.requests.get")
def test_fetch_data_success(mock_get):
    """Testet den erfolgreichen Datenabruf (Status 200)."""
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    mock_get.return_value = mock_response

    base_url = "https://api.example.com"
    endpoint = "data"
    token = "token123"

    # Act
    result = fetch_data(base_url, endpoint, token)

    # Assert
    assert result["valid"] is True
    assert result["data"] == {"result": "success"}

    # Prüfen, ob die URL korrekt zusammengebaut wurde (Slash-Handling)
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == "https://api.example.com/data"
    assert kwargs["headers"]["Authorization"] == "Bearer token123"


@patch("downloader.service.sunny_portal.requests.get")
def test_fetch_data_api_error(mock_get):
    """Testet das Verhalten bei API-Fehlern (z.B. 401 Unauthorized)."""
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    # Act
    result = fetch_data("https://api.example.com", "data", "token")

    # Assert
    assert result["valid"] is False
    assert "data" not in result


@patch("downloader.service.sunny_portal.requests.get")
def test_fetch_data_timeout(mock_get):
    """Testet, ob Timeouts abgefangen werden."""
    # Arrange
    mock_get.side_effect = requests.exceptions.Timeout("Zeitüberschreitung")

    # Act
    result = fetch_data("https://api.example.com", "data", "token")

    # Assert
    assert result["valid"] is False


@patch("downloader.service.sunny_portal.requests.get")
def test_fetch_data_connection_error(mock_get):
    """Testet, ob Verbindungsfehler abgefangen werden."""
    # Arrange
    mock_get.side_effect = requests.exceptions.ConnectionError("Verbindungsfehler")

    # Act
    result = fetch_data("https://api.example.com", "data", "token")

    # Assert
    assert result["valid"] is False
