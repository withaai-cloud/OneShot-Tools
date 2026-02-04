import sys
import os

# Add parent directory to path so we can import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app import app

# This is the WSGI handler for Vercel
# Don't reassign app - just use the imported one

