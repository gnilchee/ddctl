#!/usr/bin/env python
from datetime import datetime, timedelta

def hours_from_now(num_hours):
    # Return POSIX timestamp for number hours specified
    how_many_hours_from_now = datetime.now() + timedelta(hours=num_hours)
    return '{:%s}'.format(how_many_hours_from_now)
