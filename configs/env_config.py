"""Centralized environment configuration for all agents."""
from pathlib import Path
from dotenv import load_dotenv

def bootstrap():
    """Load environment variables from the shared .env file."""
    # Get path relative to this file's location
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)