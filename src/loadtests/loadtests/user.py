
import json
import random
import base64
from typing import Dict, Optional

import traceback

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from locust.user import HttpUser
from bs4 import BeautifulSoup

from loadtests.loadtests.config import Config
from loadtests.loadtests.constant import StatusCode
from loadtests.loadtests.user_type import UserType


class SchulcloudUser(HttpUser):

    abstract = True
    type = UserType.UNDEFINED
    weight: int = 1
    tasks: Dict = {}
    credentials: Dict[Literal['email', 'password'], str] = None

    def __init__(self, *args, **kwargs):
        super(SchulcloudUser, self).__init__(*args, **kwargs)
        self.school_id: Optional[str] = None
        self.user_id: Optional[str] = None
        self.csrf_token: Optional[str] = None
        self.bearer_token: Optional[str] = None

    @staticmethod
    def wait_time():
        return random.randint(Config.WAIT_TIME_SHORT, Config.WAIT_TIME_LONG)

    def login(self):
        """
        First task. Gets csrf token from login html website and logs in.
        Gets bearer token after login from the response header and extracts specific informations for further progress.
        """

        response = self.client.get("/login/", catch_response=True)
        soup = BeautifulSoup(response.text, "html.parser")
        self.csrf_token = soup.select_one('meta[name="csrfToken"]')['content']

        login_data = {
            "challenge": "",
            "username": self.credentials["email"],
            "password": self.credentials["password"],
            "_csrf": self.csrf_token
        }
        response = self.client.request("POST", "/login/", data=login_data, catch_response=True, allow_redirects=False)
        if response.status_code != StatusCode.REDIRECT or not response.headers.get('location').startswith("/login/success"):
            response.failure(f'Login failed: status: {response.status_code} '
                             f'({self.credentials["email"]}, headers: {response.headers})')
        else:
            self.bearer_token = response.headers["set-cookie"].split(";")[0].replace("jwt=", "")
            if len(self.bearer_token) > 12:
                token = f"{self.bearer_token[0:461]}=="
                decoded_token = base64.b64decode(token)
                decoded_token_json = json.loads(decoded_token.decode('utf-8')[30:])
                self.user_id = decoded_token_json["userId"]
                self.school_id = decoded_token_json["schoolId"]

    def logout(self):
        """
        Starts the clean-up task after stopping the loadtest and logs out the user(s) afterwards.
        """

        response = self.client.get("/logout/", allow_redirects=True)
        response.raise_for_status()
        self.bearer_token = None
        self.csrf_token = None

    def on_start(self):
        self.login()

    def on_stop(self):
        self.logout()
