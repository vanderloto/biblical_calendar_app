#!/usr/bin/env python3
"""Test web API directly."""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web', 'backend'))

from biblical_calendar.calendar_core import generate_biblical_months_dynamic

def test_web_core():
    """Test web core directly."""
    print("Testing web core directly...")
    
    df, embol, nissan = generate_biblical_months_dynamic(2025, False)
    
    print(f"Nissan: {nissan}")
    
    # Find Elul
    elul = df[df['index'] == 6].iloc[0]
    print(f"Elul: {elul['start']} - {elul['days']} days")
    
    # Print all months
    for _, row in df.iterrows():
        print(f"Month {row['index']} - {row['name']}: {row['start']}")

if __name__ == "__main__":
    test_web_core()