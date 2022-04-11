import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from pydantic.types import Json, Any


class UserFlow:
    def __init__(self):
        self.flow: google_auth_oauthlib.flow.Flow = None

    def create_flow(
            self,
            client_secrets_file: str,
            scopes: list[Any],
            state: Json,
            redirect_uri: str
    ):
        self.flow = Flow.from_client_secrets_file(
            client_secrets_file=client_secrets_file,
            scopes=scopes,
            state=state,
            redirect_uri=redirect_uri
        )

    def get_authorization_url(self, access_type='offline', prompt='consent'):
        return self.flow.authorization_url(access_type=access_type, prompt=prompt)

    def get_token(self, code: str):
        return self.flow.fetch_token(code=code)

    def get_credentials(self):
        return self.flow.credentials


if __name__ == '__main__':
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    user_flow = UserFlow()
    user_flow.create_flow(
        client_secrets_file='/Users/new/PycharmProjects/timetable-backend/calendar_backend/client_secret.json',
        scopes=SCOPES,
        state='101',
        redirect_uri='http://localhost:8000/credentials'
    )
    print(user_flow.get_authorization_url())