#!/usr/bin/env python3
"""Check what day of week is 2025-08-23."""

from datetime import date

d = date(2025, 8, 23)
print(f"2025-08-23 is a {d.strftime('%A')} (weekday: {d.weekday()}, isoweekday: {d.isoweekday()})")
# weekday(): Monday=0, Sunday=6
# isoweekday(): Monday=1, Sunday=7