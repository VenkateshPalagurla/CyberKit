import pytest
import requests
from unittest.mock import patch, MagicMock
import tools.email_leak as email_leak
from io import StringIO
import sys

# Helper to capture printed output from a function
def capture_output(func, *args):
    captured = StringIO()
    sys.stdout = captured
    func(*args)
    sys.stdout = sys.__stdout__
    return captured.getvalue()

@patch("tools.email_leak.requests.get")
def test_breaches_found(mock_get):
    """Test: API returns breach data"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "Title": "TestBreach",
            "Domain": "test.com",
            "BreachDate": "2023-01-01",
            "PwnCount": 12345,
            "Description": "Test description <br> with HTML",
            "DataClasses": ["Emails", "Passwords"]
        }
    ]

    output = capture_output(email_leak.check_email_leak, "test@example.com")
    print("\ntest_breaches_found OUTPUT:\n", output)
    assert "[!] Found 1 breach" in output
    assert "== Breach: TestBreach ==" in output
    assert "Data leaked : Emails, Passwords" in output
    assert "Description" in output and "Test description" in output

@patch("tools.email_leak.requests.get")
def test_no_breaches_found(mock_get):
    """Test: No breaches found (HTTP 404)"""
    mock_get.return_value.status_code = 404
    output = capture_output(email_leak.check_email_leak, "clean@example.com")
    print("\ntest_no_breaches_found OUTPUT:\n", output)
    assert "no breaches found" in output.lower()

@patch("tools.email_leak.requests.get")
def test_invalid_api_key(mock_get):
    """Test: Invalid API key (HTTP 401)"""
    mock_get.return_value.status_code = 401
    output = capture_output(email_leak.check_email_leak, "test@example.com")
    print("\ntest_invalid_api_key OUTPUT:\n", output)
    assert "unauthorized" in output.lower()

@patch("tools.email_leak.requests.get")
def test_rate_limit(mock_get):
    """Test: Rate limit hit (HTTP 429)"""
    mock_get.return_value.status_code = 429
    output = capture_output(email_leak.check_email_leak, "test@example.com")
    print("\ntest_rate_limit OUTPUT:\n", output)
    assert "rate limit" in output.lower()

@patch("tools.email_leak.requests.get")
def test_api_failure(mock_get):
    """Test: Unexpected API status code"""
    mock_get.return_value.status_code = 500
    output = capture_output(email_leak.check_email_leak, "test@example.com")
    print("\ntest_api_failure OUTPUT:\n", output)
    assert "unexpected error" in output.lower()

@patch("tools.email_leak.requests.get")
def test_request_exception(mock_get):
    """Test: Network error or failed request"""
    mock_get.side_effect = requests.exceptions.RequestException("Connection failed")
    output = capture_output(email_leak.check_email_leak, "test@example.com")
    print("\ntest_request_exception OUTPUT:\n", output)
    assert "request failed" in output.lower()
