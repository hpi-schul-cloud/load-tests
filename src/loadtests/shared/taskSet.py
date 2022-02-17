
from curses.ascii import HT
import requests
from locust.user import HttpUser
from locust.user.task import TaskSet
from locust.env import Environment
from locust.main import create_environment

from loadtests.loadtests.locustfile import AdminUser
from loadtests.loadtests.scTaskSet import scTaskSet


class Interface:
    
    def __init__(self) -> None:
        self.login = None
        self.requests_client = requests.Session()
    
    def interrupt(self):
        pass

class TaskSetSchulCloud:

    def __init__(self, interface: Interface) -> None:
        self.interface: Interface = interface

    def login(self):
        if not self.login:
            self.interface.interrupt()
