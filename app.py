from email import message
from urllib.parse import unquote
import os
import datetime

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.templating import Jinja2Templates
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials
from pydantic.types import Json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from db import Credentials
from settings import Settings
from flow import UserFlow

settings = Settings()
app = FastAPI(root_path=settings.APP_URL)
templates = Jinja2Templates(directory="/Users/new/PycharmProjects/timetable-webapp/templates")
app.add_middleware(DBSessionMiddleware, db_url=settings.DB_DSN)
user_flow = UserFlow()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "groups": settings.GROUPS,
            "google_creds": settings.GOOGLE_CREDS,
        },
    )


@app.get("/flow")
def get_user_flow(state: str):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    user_flow.create_flow(
        client_secrets_file='/Users/new/PycharmProjects/timetable-backend/calendar_backend/client_secret.json',
        scopes=SCOPES,
        state=state,
        redirect_uri='http://localhost:8000/credentials'
    )
    return RedirectResponse(user_flow.get_authorization_url()[0])


@app.get("/credentials")
def get_credentials(
        background_tasks: BackgroundTasks,
        code: str,
        scope: str,
        state: Json,
):
    scope = scope.split(unquote("%20"))
    group = state.get("group")
    user_flow.get_token(code=code)
    creds = user_flow.get_credentials()
    token: Json = creds.to_json()

    if not group:
        raise HTTPException(403, "No group provided")

    #db_records = db.session.query(Credentials)
    # write all to db
    # for further sessoin creation you will need only token

    return RedirectResponse(settings.REDIRECT_URL)
