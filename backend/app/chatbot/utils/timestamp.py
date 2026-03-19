"""Timestamp formatting utilities."""
from datetime import datetime


def format_timestamp(timestamp: float) -> str:
    """
    Format a timestamp into a human-readable datetime string.
    
    Args:
        timestamp: Unix timestamp (seconds since epoch)
        
    Returns:
        Formatted datetime string in the format 'YYYY-MM-DD HH:MM:SS'
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")
