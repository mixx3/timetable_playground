import json
import os
import json
from pydantic import BaseSettings, Json, PostgresDsn, AnyHttpUrl
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings"""

    DB_DSN: PostgresDsn = os.getenv("FFPOSTGRES_DSN")
    PATH_TO_GOOGLE_CREDS: str = os.getenv('PATH_TO_CREDS')
    APP_URL: Optional[AnyHttpUrl] = None
    REDIRECT_URL: AnyHttpUrl = "https://www.profcomff.com"
    GROUPS: List[str] = ["101", "102"]
    DEFAULT_GROUP = '{group: 101}'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"
