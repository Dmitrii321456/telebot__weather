import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BOT_KEY = os.getenv('SECRET_KEY')
