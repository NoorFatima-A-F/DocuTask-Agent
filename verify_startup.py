"""
Startup Import & Verification Script.
Imports app.main to verify all modules, models, services, dependencies, and FastAPI instances instantiate with 0 errors.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    print("Testing application imports...")
    import app.main
    print("✓ SUCCESS: app.main imported cleanly without any errors.")
    print(f"Project Title: {app.main.app.title}")
except Exception as e:
    print(f"✗ FAILURE: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
