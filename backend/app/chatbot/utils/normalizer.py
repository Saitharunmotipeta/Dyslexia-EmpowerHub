"""Normalization utilities for timestamps and comparable values."""
from datetime import datetime


def normalize(dt):
    """
    Normalize a datetime object to a Unix timestamp for comparison.
    
    Args:
        dt: Datetime object to normalize
        
    Returns:
        Unix timestamp (float) for comparison purposes
    """
    if dt is None:
        return 0
    
    if isinstance(dt, datetime):
        return dt.timestamp()
    
    return dt
