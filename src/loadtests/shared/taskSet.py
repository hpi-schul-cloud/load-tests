
from curses.ascii import HT
from re import S
from signal import set_wakeup_fd
from typing_extensions import runtime
from locust import task
import requests
from locust.user import HttpUser
from locust.user.task import TaskSet
from locust.env import Environment
from locust.main import create_environment
from bs4 import BeautifulSoup
import base64
import json
from loadtests.loadtests.functions import deleteDoc
from loadtests.shared.constant import Constant
from loadtests.loadtests.locustfile import AdminUser
from loadtests.loadtests.scTaskSet import scTaskSet


class Interface:
    
    def __init__(self) -> None:
        self.login = None
        self.requests_client = requests.Session()
        self.base_url = None
        self.csrf_token = None
        self.user_id = None
        self.school_id = None
        self.user_typ = None
        self.createdDocuments = None
        self.user_host = None
        self.createdCourses = None
        self.createdTeams = None


    
    def interrupt(self):
        pass
    

class TaskSetSchulCloud:

    def __init__(self, interface: Interface) -> None:
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
                'password' : self.login['passwort'],
                '_csrf' : self.interface.csrf_token
        }    

        response = self.interface.requests_client.post('/login/', data=login_data, catch_response=True, allow_redirects=False)
        if (response.status_code != Constant.returncodeRedirect) or not response.heasers.get('location').startswith("/login/success"):
           raise RuntimeError(f'Login failed: bad status code ({response.status_code})')
        else:
            response_header = response.headers
            #Extracting BearerToken from Responses Header
            bearer_token = (response_header["set-cookie"]).split(";")[0].replace("jwt=", "")
            if len(bearer_token) > 12:
                token = (bearer_token)[0:461] + "=="
                decoded_token = base64.b64decode(token)
                decoded_token_json = json.loads(decoded_token.decode('utf-8')[30:])
                self.interface.user_id = decoded_token_json["userId"]
                self.interface.school_id = decoded_token_json["schoolId"]

    def logout(self):        
        '''
        Starts the clean-up task after stopping the loadtest and logs out the user(s) afterwards.
        '''
        self.cleanUpLoadtest(self)
        self.interface.requests_client.get('/logout/', allow_redirects=True)
        self.interface.csrf_token = None
    
    def cleanUpLoadtest(self):
        '''
        Deletes all remaining documents, courses and teams which were created through the loadtest and keeps the stageing-test-area clean.
        Skips if no document-, course- our team- ID found.
        '''
        if self.interface.user_typ == 'teacher':

            for documentId in self.interface.createdDocuments:
                url = f"{self.interface.user_host}/files/my/"
                with self.interface.requests_client.get(url, catch_response=True, allow_redirects=True) as response:
                    soup = BeautifulSoup(response.text, "html.parser")
                    findId = soup.find_all("div", {"data-file-id" : documentId})    # Searches document id on html page
                    if len(findId) > 0:
                        self.deleteDoc(documentId)
                self.createdDocuments = None

            for courseId in self.interface.createdCourses:
                url = f"{self.interface.user_host}/cources/"
                with self.interface.requests_client.get(url, catch_response=True, allow_redirects=True) as response:
                    soup = BeautifulSoup(response.text, "html.parser")
                    findId = soup.find_all("div", {"data-id" : courseId}) # Searches course id on html page
                if len(findId) > 0:
                    self.deleteCourse(courseId)
            self.createdCourses = None

            for teamId in self.interface.createdTeams:
                url = f"{self.interface.user_host}/teams/"
                with self.interface.requests_client.get(url, catch_response=True, allow_redirects=True) as response:
                    soup = BeautifulSoup(response.text, "html.parser")
                    findId = soup.find_all({"data-id":teamId})
                if not findId is None:
                    self.deleteTeam(teamId)
            self.createdTeams = None



    
    
    def deleteDoc(self, documentId):
        pass
    
    def deleteCourse(self, courseId):
        pass

    def deleteTeam(self, teamId):
        pass

