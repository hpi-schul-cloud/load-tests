
from typing import TypedDict
from re import S

from curses.ascii import HT
from signal import set_wakeup_fd
import requests
from locust.user import HttpUser
from locust.user.task import TaskSet
from locust.env import Environment
from locust.main import create_environment
from bs4 import BeautifulSoup

from loadtests.shared.constant import Constant
from loadtests.loadtests.locustfile import AdminUser
from loadtests.loadtests.scTaskSet import scTaskSet


Login = TypedDict('Login', {'email': str, 'password': str})


class Interface:
    
    def __init__(self):
        self.login: Login = None
        self.requests_client: requests.Session = None
        self.base_url: str = None
        self.csrf_token: str = None
    
    def interrupt(self):
        pass
    

class TaskSetSchulCloud(TaskSet):

    def __init__(self, parent, creator_is_locust=True):
        super(TaskSetSchulCloud, self).__init__(parent)
        self.interface: Interface = interface

    @property
    def base_url(self):
        return self.interface.base_url
    
    def login(self):
        if not self.login:
            self.interface.interrupt()
        response = self.interface.requests_client.get(self.base_url + "/login/")
        soup = BeautifulSoup(response.text, 'html.parser')
        self.interface.csrf_token = soup.select_one('meta[name="csrfToken"]')['content']

        login_data = {
                'challenge' : '',
                'username' : self.login['email'],
                'password' : self.login['password'],
                '_csrf' : self.interface.csrf_token
        }    

        response = self.interface.requests_client.post('/login/', data=login_data, catch_response=True, allow_redirects=False)
        if (response.status_code != Constant.returncodeRedirect) or not response.heasers.get('location').startswith("/login/success"):
           pass
