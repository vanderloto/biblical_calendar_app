"""Test script to verify backend imports work correctly."""

import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    print("Testing imports...")
    
    # Test Flask
    from flask import Flask
    print("✅ Flask imported successfully")
    
    # Test numpy
    import numpy as np
    print(f"✅ NumPy {np.__version__} imported successfully")
    
    # Test skyfield
    from skyfield import api
    print("✅ Skyfield imported successfully")
    
    # Test biblical calendar
    from biblical_calendar.calendar import generate_biblical_months_dynamic
    print("✅ Biblical calendar module imported successfully")
    
    # Test app
    import app
    print("✅ App module imported successfully")
    
    print("\n🎉 All imports successful! Backend is ready.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 Try installing compatible versions:")
    print("pip install 'numpy<2.0' --upgrade")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)