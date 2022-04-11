import json
import os
import json
from pydantic import BaseSettings, Json, PostgresDsn, AnyHttpUrl
from typing import List, Optional

with open('/Users/new/PycharmProjects/timetable-webapp/client_secret.json') as jfp:
    json_str = jfp.read()


class Settings(BaseSettings):
    """Application settings"""

    DB_DSN: PostgresDsn = os.getenv("FFPOSTGRES_DSN")
    GOOGLE_CREDS: Json = json_str
    APP_URL: Optional[AnyHttpUrl] = None
    REDIRECT_URL: AnyHttpUrl = "https://www.profcomff.com"
    GROUPS: List[str] = ["101", "102"]

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"
