def make_rows(dates):
    return [{"Date": d, "Description": "desc", "Amount": "1.0", "Transaction_Type": "DEBIT"} for d in dates]

class TestValidateCSVDateRange:
    def test_all_dates_in_range(self):
        from silver_garbanzo.contracts import validate_csv_date_range
        from datetime import datetime
        rows = make_rows(["2026-01-01", "2026-01-15", "2026-01-31"])
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 31)
        validate_csv_date_range(rows, start, end)

    def test_date_out_of_range(self):
        from silver_garbanzo.contracts import validate_csv_date_range
        from datetime import datetime
        rows = make_rows(["2026-01-01", "2026-02-01", "2026-01-31"])
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 31)
        import pytest
        with pytest.raises(ValueError, match="outside filename-declared range"):
            validate_csv_date_range(rows, start, end)

    def test_invalid_date_format(self):
        from silver_garbanzo.contracts import validate_csv_date_range
        from datetime import datetime
        rows = make_rows(["2026-01-01", "bad-date", "2026-01-31"])
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 31)
        import pytest
        with pytest.raises(ValueError, match="Invalid date format"):
            validate_csv_date_range(rows, start, end)
"""
test_contracts.py — Tests for filename and contract validation.
"""

from datetime import datetime

import pytest

from silver_garbanzo.contracts import FilenameRange, parse_filename_range


class TestParseFilenameRangeMonthly:
    """Test parsing of monthly format: <account>__YYYY-MM.csv"""
    
    def test_valid_monthly_format(self):
        """Parse valid monthly filename."""
        result = parse_filename_range("checking__2026-01.csv")
        assert result.account == "checking"
        assert result.start_date == datetime(2026, 1, 1)
        assert result.end_date == datetime(2026, 1, 31)
        assert result.filename == "checking__2026-01.csv"
    
    def test_valid_monthly_format_december(self):
        """Parse valid monthly filename for December (edge case)."""
        result = parse_filename_range("savings__2025-12.csv")
        assert result.account == "savings"
        assert result.start_date == datetime(2025, 12, 1)
        assert result.end_date == datetime(2025, 12, 31)
    
    def test_valid_monthly_format_february(self):
        """Parse valid monthly filename for February (leap year edge case)."""
        result = parse_filename_range("checking__2024-02.csv")
        assert result.account == "checking"
        assert result.start_date == datetime(2024, 2, 1)
        assert result.end_date == datetime(2024, 2, 29)
    
    def test_valid_monthly_format_february_non_leap(self):
        """Parse valid monthly filename for February non-leap year."""
        result = parse_filename_range("checking__2025-02.csv")
        assert result.account == "checking"
        assert result.start_date == datetime(2025, 2, 1)
        assert result.end_date == datetime(2025, 2, 28)
    
    def test_account_with_underscores(self):
        """Account names can contain underscores."""
        result = parse_filename_range("my_checking_account__2026-01.csv")
        assert result.account == "my_checking_account"
    
    def test_invalid_month(self):
        """Fail on invalid month."""
        with pytest.raises(ValueError, match="Invalid date in monthly filename"):
            parse_filename_range("checking__2026-13.csv")
    
    def test_invalid_month_zero(self):
        """Fail on month zero."""
        with pytest.raises(ValueError, match="Invalid date in monthly filename"):
            parse_filename_range("checking__2026-00.csv")
    
    def test_missing_extension(self):
        """Parse filename without .csv extension."""
        result = parse_filename_range("checking__2026-01")
        assert result.account == "checking"
        assert result.start_date == datetime(2026, 1, 1)


class TestParseFilenameRangeExplicit:
    """Test parsing of explicit range format: <account>__YYYY-MM-DD__YYYY-MM-DD.csv"""
    
    def test_valid_explicit_range_format(self):
        """Parse valid explicit range filename."""
        result = parse_filename_range("checking__2026-01-15__2026-02-14.csv")
        assert result.account == "checking"
        assert result.start_date == datetime(2026, 1, 15)
        assert result.end_date == datetime(2026, 2, 14)
    
    def test_valid_explicit_range_same_day(self):
        """Parse explicit range with same start and end date."""
        result = parse_filename_range("checking__2026-01-15__2026-01-15.csv")
        assert result.account == "checking"
        assert result.start_date == datetime(2026, 1, 15)
        assert result.end_date == datetime(2026, 1, 15)
    
    def test_invalid_explicit_range_start_after_end(self):
        """Fail when start date is after end date."""
        with pytest.raises(ValueError, match="Start date .* is after end date"):
            parse_filename_range("checking__2026-02-14__2026-01-15.csv")
    
    def test_invalid_day_in_explicit_range(self):
        """Fail on invalid day in explicit range."""
        with pytest.raises(ValueError, match="Invalid date range"):
            parse_filename_range("checking__2026-02-30__2026-03-01.csv")
    
    def test_account_with_dashes(self):
        """Account names can contain dashes."""
        result = parse_filename_range("my-checking__2026-01-01__2026-01-31.csv")
        assert result.account == "my-checking"


class TestParseFilenameRangeInvalid:
    """Test invalid filename formats."""
    
    def test_no_account(self):
        """Fail when account is missing."""
        with pytest.raises(ValueError, match="does not match supported formats"):
            parse_filename_range("__2026-01.csv")
    
    def test_missing_separators(self):
        """Fail on missing separators."""
        with pytest.raises(ValueError, match="does not match supported formats"):
            parse_filename_range("checking2026-01.csv")
    
    def test_wrong_format(self):
        """Fail on completely wrong format."""
        with pytest.raises(ValueError, match="does not match supported formats"):
            parse_filename_range("checking.2026.01.csv")
    
    def test_empty_string(self):
        """Fail on empty filename."""
        with pytest.raises(ValueError, match="does not match supported formats"):
            parse_filename_range("")
    
    def test_only_extension(self):
        """Fail on only extension."""
        with pytest.raises(ValueError, match="does not match supported formats"):
            parse_filename_range(".csv")
    
    def test_partial_date_format(self):
        """Fail on partial date (e.g., only year)."""
        with pytest.raises(ValueError, match="does not match supported formats"):
            parse_filename_range("checking__2026.csv")
    
    def test_too_many_double_underscores(self):
        """Fail on too many separators."""
        with pytest.raises(ValueError, match="does not match supported formats"):
            parse_filename_range("checking__2026-01__2026-02__extra.csv")


class TestParseFilenameRangeReturnType:
    """Test return type structure."""
    
    def test_returns_named_tuple(self):
        """Result is a FilenameRange named tuple."""
        result = parse_filename_range("checking__2026-01.csv")
        assert isinstance(result, FilenameRange)
        assert hasattr(result, 'account')
        assert hasattr(result, 'start_date')
        assert hasattr(result, 'end_date')
        assert hasattr(result, 'filename')
    
    def test_named_tuple_fields_are_correct_types(self):
        """Named tuple fields have correct types."""
        result = parse_filename_range("checking__2026-01-15__2026-02-14.csv")
        assert isinstance(result.account, str)
        assert isinstance(result.start_date, datetime)
        assert isinstance(result.end_date, datetime)
        assert isinstance(result.filename, str)
