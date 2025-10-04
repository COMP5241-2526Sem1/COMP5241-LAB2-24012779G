"""
Vercel Entry Point for NoteTaker Flask Application
"""
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Import the Flask app - Vercel expects 'app' variable
from src.main import app

# Export for Vercel
app = app