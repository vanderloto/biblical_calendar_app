#!/usr/bin/env python3
"""Debug script to compare date calculations between desktop and web versions."""

import sys
import os
from datetime import datetime, date

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import both versions
from biblical_calendar.calendar import generate_biblical_months_dynamic as desktop_generate
from biblical_calendar.calendar_core import generate_biblical_months_dynamic as web_generate

def debug_calculations():
    """Compare calculations between desktop and web versions."""
    year = 2025
    
    print(f"=== DEBUG BIBLICAL CALENDAR CALCULATIONS FOR {year} ===\n")
    
    # Desktop version
    print("DESKTOP VERSION:")
    try:
        desktop_df, desktop_embol, desktop_nissan = desktop_generate(year, False)
        print(f"Nissan start: {desktop_nissan}")
        
        # Find Elul (month 6)
        elul_desktop = desktop_df[desktop_df['index'] == 6].iloc[0]
        print(f"Elul (month 6): {elul_desktop['start']} - {elul_desktop['days']} days")
        
    except Exception as e:
        print(f"Desktop error: {e}")
    
    print("\nWEB VERSION:")
    try:
        web_df, web_embol, web_nissan = web_generate(year, False)
        print(f"Nissan start: {web_nissan}")
        
        # Find Elul (month 6)
        elul_web = web_df[web_df['index'] == 6].iloc[0]
        print(f"Elul (month 6): {elul_web['start']} - {elul_web['days']} days")
        
    except Exception as e:
        print(f"Web error: {e}")
    
    print("\n=== COMPARISON ===")
    try:
        if desktop_nissan == web_nissan:
            print("✅ Nissan dates match")
        else:
            print(f"❌ Nissan dates differ: Desktop={desktop_nissan}, Web={web_nissan}")
        
        if elul_desktop['start'] == elul_web['start']:
            print("✅ Elul dates match")
        else:
            print(f"❌ Elul dates differ: Desktop={elul_desktop['start']}, Web={elul_web['start']}")
            
    except Exception as e:
        print(f"Comparison error: {e}")

if __name__ == "__main__":
    debug_calculations()