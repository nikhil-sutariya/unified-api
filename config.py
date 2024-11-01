from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import load_dotenv
import os
import logging
load_dotenv()

LOG_LEVEL = logging.DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

log_file = os.path.join(os.getcwd(), "app.log")
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

CLIENT_ORIGINS = list(filter(None, os.getenv("CLIENT_ORIGINS").split(",")))

class Settings(BaseSettings):
    app_title: str
    app_version: str
    client_origin: list = CLIENT_ORIGINS
    host_url: str
    smtp_email_from: str
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()
