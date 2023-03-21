import os
from generate_env import get_env
from settings import SCOPES
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Authenticator:
    def __init__(self,
                 creds_path: str = "../credentials.json",
                 scopes: list[str] = None):

        if scopes is None:
            self.scopes: list[str] = SCOPES
        self.creds_file = creds_path
        self._creds = None
        self._is_token_generated = True if os.path.exists('../token.json') else False
        self._is_env_generated = True if os.path.exists('../.env') else False

    def generate_creds(self):
        if self._is_token_generated:
            self._creds = Credentials.from_authorized_user_file('../token.json', self.scopes)
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("./expenses_tracker/credentials.json", self.scopes)
                self._creds = flow.run_local_server()
            with open('../token.json', 'w') as token:
                token.write(self._creds.to_json())
                self._is_token_generated = True

    def generate_env(self) -> None:
        if not self.is_env_generated:
            get_env(creds_filename=self.creds_file)
            self._is_env_generated = True

    def get_service(self):
        if self._creds is not None:
            return build('gmail', 'v1', credentials=self._creds)
        self.generate_creds()
        return build('gmail', 'v1', credentials=self._creds)

    @property
    def is_token_generated(self) -> bool:
        return self._is_token_generated

    @property
    def is_env_generated(self) -> bool:
        return self._is_env_generated
