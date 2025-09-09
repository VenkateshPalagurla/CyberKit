import io
import sys
import builtins
import re
from unittest.mock import patch
import tools.ip_lookup as ip_lookup
import requests  # Needed for proper exception types

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Capture printed output from a function
def capture_output(func, *args, **kwargs):
    out = io.StringIO()
    original_print = builtins.print
    builtins.print = lambda *x, **kw: original_print(*x, **{**kw, "file": out})
    try:
        func(*args, **kwargs)
    finally:
        builtins.print = original_print
    return out.getvalue()


# Ensure HTTP 404/500 API errors print a message
def test_valid_ip_api_error():
    with patch("tools.ip_lookup.requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.reason = "Not Found"
        output = capture_output(ip_lookup.run, "1.2.3.4")
        assert "API Error" in output or "Failed to retrieve" in output


# Test invalid IP string is caught
def test_invalid_ip_format():
    output = capture_output(ip_lookup.run, "999.999.999.999")
    assert "Invalid IP address format" in output


# Simulate network error using correct exception type
def test_request_exception_handling():
    with patch("tools.ip_lookup.requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("Connection failed")
        output = capture_output(ip_lookup.run, "8.8.8.8")
        assert "Request error" in output or "Failed to retrieve" in output


# Simulate timeout using requests.Timeout
def test_timeout_handling():
    with patch("tools.ip_lookup.requests.get") as mock_get:
        mock_get.side_effect = requests.Timeout("Timeout")
        output = capture_output(ip_lookup.run, "8.8.8.8")
        assert "Timeout" in output or "Request error" in output

# Test when API returns malformed JSON
def test_malformed_json_response():
    with patch("tools.ip_lookup.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("Malformed JSON")
        output = capture_output(ip_lookup.run, "8.8.8.8")
        clean = strip_ansi(output)
        assert "Received malformed JSON" in clean


