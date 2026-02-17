"""module tests.service.sunny_portal"""

from datetime import datetime
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
    assert headers["sec-ch-ua-mobile"] == "?0"


@patch("downloader.service.sunny_portal.requests.post")
def test_fetch_data_success(mock_post):
    """Testet den erfolgreichen Datenabruf (Status 200)."""
    # Arrange
    mock_response_1 = Mock()
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = [{"channelId": "Channel.1", "values": []}]

    mock_response_2 = Mock()
    mock_response_2.status_code = 200
    mock_response_2.json.return_value = [{"channelId": "Channel.2", "values": []}]

    mock_post.side_effect = [mock_response_1, mock_response_2]

    api_data = {
        "api_base_url": "https://api.example.com",
        "endpoint": "data",
        "authorization_token": "token123",
    }
    device_data = {
        "component_id": "12345",
        "resolution": "FiveMinutes",
        "channel_ids": ["Channel.1", "Channel.2"],
    }
    start = datetime(2026, 1, 30, 23, 0, 0)
    end = datetime(2026, 2, 13, 23, 0, 0)

    # Act
    result = fetch_data(api_data, device_data, start, end)

    # Assert
    # valid ist True, wenn alle Requests erfolgreich waren
    # (oder zumindest Daten da sind, je nach Logik)
    # Im Code oben setzen wir es auf False, wenn einer fehlschlägt, hier sind beide 200 OK.
    assert result["valid"] is True
    assert len(result["data"]) == 2
    assert result["data"][0]["channelId"] == "Channel.1"
    assert result["data"][1]["channelId"] == "Channel.2"

    # Prüfen, ob post zweimal aufgerufen wurde
    assert mock_post.call_count == 2

    # Argumente des ersten Aufrufs prüfen
    args, kwargs = mock_post.call_args_list[0]
    assert args[0] == "https://api.example.com/data"
    assert kwargs["headers"]["Authorization"] == "Bearer token123"
    assert len(kwargs["json"]["queryItems"]) == 1
    assert kwargs["json"]["queryItems"][0]["channelId"] == "Channel.1"
    assert kwargs["json"]["dateTimeBegin"] == "2026-01-30T23:00:00.000Z"


@patch("downloader.service.sunny_portal.get_new_token")
@patch("downloader.service.sunny_portal.requests.post")
def test_fetch_data_token_refresh_success(mock_post, mock_get_token):
    """Testet, ob der Token bei einem 401-Fehler erfolgreich erneuert wird."""
    # Arrange
    # First call returns 401, second call (after token refresh) returns 200
    mock_response_401 = Mock()
    mock_response_401.status_code = 401

    mock_response_200 = Mock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = [{"channelId": "Channel.1", "values": [1, 2]}]

    mock_post.side_effect = [mock_response_401, mock_response_200]

    # Mock the token refresh function to return a new token
    mock_get_token.return_value = "new_refreshed_token"

    api_data = {
        "api_base_url": "https://api.example.com",
        "endpoint": "data",
        "authorization_token": "old_expired_token",
        "username": "user",
        "password": "pw",
    }
    device_data = {
        "component_id": "123",
        "resolution": "PT5M",
        "channel_ids": ["Channel.1"],
    }
    start = datetime(2026, 1, 30, 23, 0, 0)
    end = datetime(2026, 2, 13, 23, 0, 0)

    # Act
    result = fetch_data(api_data, device_data, start, end)

    # Assert
    assert result["valid"] is True
    assert len(result["data"]) == 1
    assert result["data"][0]["values"] == [1, 2]

    # Check that mocks were called
    mock_get_token.assert_called_once()
    assert mock_post.call_count == 2

    # Check that the second call used the new token
    second_call_kwargs = mock_post.call_args_list[1][1]
    assert second_call_kwargs["headers"]["Authorization"] == "Bearer new_refreshed_token"


@patch("downloader.service.sunny_portal.get_new_token")
@patch("downloader.service.sunny_portal.requests.post")
def test_fetch_data_token_refresh_fails(mock_post, mock_get_token):
    """Testet das Verhalten, wenn der Token-Refresh fehlschlägt."""
    # Arrange
    mock_response_401 = Mock()
    mock_response_401.status_code = 401
    mock_post.return_value = mock_response_401  # Always return 401

    # Mock the token refresh function to return None (failure)
    mock_get_token.return_value = None

    api_data = {
        "api_base_url": "https://api.example.com",
        "endpoint": "data",
        "authorization_token": "old_expired_token",
        "username": "user",
        "password": "pw",
    }
    device_data = {
        "component_id": "123",
        "resolution": "PT5M",
        "channel_ids": ["Channel.1"],
    }
    start = datetime(2026, 1, 30, 23, 0, 0)
    end = datetime(2026, 2, 13, 23, 0, 0)

    # Act
    result = fetch_data(api_data, device_data, start, end)

    # Assert
    assert result["valid"] is False
    assert "data" not in result
    mock_get_token.assert_called_once()
    mock_post.assert_called_once()  # Only called once, because refresh failed and it broke the loop


@patch("downloader.service.sunny_portal.requests.post")
def test_fetch_data_timeout(mock_post):
    """Testet, ob Timeouts abgefangen werden."""
    # Arrange
    mock_post.side_effect = requests.exceptions.Timeout("Zeitüberschreitung")

    api_data = {
        "api_base_url": "https://api.example.com",
        "endpoint": "data",
        "authorization_token": "token",
        "username": "user",
        "password": "pw",
    }
    device_data = {
        "component_id": "123",
        "resolution": "PT5M",
        "channel_ids": ["Channel.1"],
    }
    start = datetime(2026, 1, 30, 23, 0, 0)
    end = datetime(2026, 2, 13, 23, 0, 0)

    # Act
    result = fetch_data(api_data, device_data, start, end)

    # Assert
    assert result["valid"] is False


@patch("downloader.service.sunny_portal.requests.post")
def test_fetch_data_connection_error(mock_post):
    """Testet, ob Verbindungsfehler abgefangen werden."""
    # Arrange
    mock_post.side_effect = requests.exceptions.ConnectionError("Verbindungsfehler")

    api_data = {
        "api_base_url": "https://api.example.com",
        "endpoint": "data",
        "authorization_token": "token",
        "username": "user",
        "password": "pw",
    }
    device_data = {
        "component_id": "123",
        "resolution": "PT5M",
        "channel_ids": ["Channel.1"],
    }
    start = datetime(2026, 1, 30, 23, 0, 0)
    end = datetime(2026, 2, 13, 23, 0, 0)

    # Act
    result = fetch_data(api_data, device_data, start, end)

    # Assert
    assert result["valid"] is False
