from django.utils import timezone

from datetime import timezone as dt_timezone

import zoneinfo

MANILA_TZ = zoneinfo.ZoneInfo("Asia/Manila")

def get_manila_time(dt=None):
    """
    Convert a UTC datetime to Asia/Manila timezone.

    If dt is None, uses current UTC time.
    """
    if dt is None:
        dt = timezone.now()

    # Ensure datetime is timezone-aware (Django uses UTC by default)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.utc)

    return timezone.localtime(dt, MANILA_TZ)

def manila_to_utc(dt):
    """
    Convert Asia/Manila time to UTC.
    """
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, MANILA_TZ)
    else:
        dt = dt.astimezone(MANILA_TZ)

    return dt.astimezone(dt_timezone.utc)