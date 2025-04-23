from datetime import datetime
from typing import Optional


def parse_date(date_str: str) -> Optional[datetime]:
    """Helper function to parse date strings into datetime objects.
    Handles common formats found in the data. Returns None if parsing fails.
    """
    try:
        return datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None
