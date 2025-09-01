#!/usr/bin/env python3
"""Debug moon calculations."""

import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from biblical_calendar.calendar_core import (
    next_new_moon_on_or_after, 
    get_march_equinox,
    TS, 
    Eph,
    almanac
)

def debug_moon_phases():
    """Debug specific moon calculations for Elul."""
    year = 2025
    
    print(f"=== DEBUGGING MOON PHASES FOR {year} ===")
    
    # Get equinox
    equinox = get_march_equinox(year)
    print(f"March equinox: {equinox}")
    
    # Get Nissan start
    nissan_start = next_new_moon_on_or_after(equinox)
    print(f"Nissan start (1st new moon): {nissan_start}")
    
    # Calculate all new moons for the year
    new_moons = [nissan_start]
    cursor = nissan_start + timedelta(days=1)
    
    for i in range(12):
        nm = next_new_moon_on_or_after(cursor)
        new_moons.append(nm)
        cursor = nm + timedelta(days=1)
        print(f"Month {i+2} new moon: {nm}")
    
    print(f"\nElul (month 6) should start: {new_moons[5]}")
    
    # Also check raw Skyfield calculation for that specific date
    print("\n=== RAW SKYFIELD CHECK ===")
    t0 = TS.utc(2025, 8, 20)  # Around expected date
    t1 = TS.utc(2025, 8, 25)
    f = almanac.moon_phases(Eph)
    times, phases = almanac.find_discrete(t0, t1, f)
    
    for ti, ph in zip(times, phases):
        if ph == 0:  # New moon
            dt = ti.utc_datetime()
            print(f"Raw new moon: {dt} -> date: {dt.date()}")

if __name__ == "__main__":
    debug_moon_phases()