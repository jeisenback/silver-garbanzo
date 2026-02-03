"""
test_headers.py — Tests for CSV header validation contract.
"""

import pytest

from silver_garbanzo.contracts import REQUIRED_HEADERS, validate_csv_headers


class TestValidateCSVHeaders:
    """Test CSV header validation."""

    def test_valid_headers(self):
        # Exact match
        validate_csv_headers(REQUIRED_HEADERS)

    def test_missing_header(self):
        headers = ["Date", "Description", "Amount"]  # Missing Transaction_Type
        with pytest.raises(ValueError, match="Missing required header"):
            validate_csv_headers(headers)

    def test_all_missing(self):
        headers = []
        with pytest.raises(ValueError, match="Missing required header"):
            validate_csv_headers(headers)

    # Uncomment to test strict schema (no extra headers)
    # def test_extra_header(self):
    #     headers = REQUIRED_HEADERS + ["Extra"]
    #     with pytest.raises(ValueError, match="Unexpected header"):
    #         validate_csv_headers(headers)
