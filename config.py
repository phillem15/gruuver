import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ENV = os.getenv('ENV')
    SECRET = os.getenv('SECRET')
    API_URL = os.getenv('API_URL')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
