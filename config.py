import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ENV = os.getenv('ENV')
    SECRET = os.getenv('SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    PORT = os.getenv('PORT')
    API_URL = os.getenv('API_URL')
