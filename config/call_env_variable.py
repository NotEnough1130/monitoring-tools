import logging
import os
from pathlib import Path
from dotenv import load_dotenv

#Start logging
logging.basicConfig(level=logging.INFO)

def get_env(key):
    env_path = Path('../config/.env')
    load_dotenv(dotenv_path=env_path)
    return os.getenv(key)
