import base64
import os
import json
import urllib.request
import stat
import zipfile
from loadtests import constant

from loadtests.functions import *
from bs4 import BeautifulSoup

def login(self):
    '''
    First task. Gets csrf token from login html website and logs in.
    Gets bearer token after login from the response header and extracts specific informations for further progress.
    '''

    if self.user.login_credentials == None:
        self.interrupt(reschedule=False)

    with self.client.get("/login/", catch_response=True) as login_get_response:
        soup = BeautifulSoup(login_get_response.text, "html.parser")
        self.csrf_token = soup.select_one('meta[name="csrfToken"]')['content']

        login_data = {
            "challenge" : "",
            "username"  : self.user.login_credentials["email"],
            "password"  : self.user.login_credentials["password"],
            "_csrf"     : self.csrf_token
        }
        with self.client.request("POST", "/login/", data=login_data, catch_response=True, allow_redirects=False)  as login_post_response:
            if (login_post_response.status_code != constant.constant.returncodeRedirect) or not login_post_response.headers.get('location').startswith("/login/success"):
                login_post_response.failure("Failed! (username: " + self.user.login_credentials["email"] + ", http-code: "+str(login_post_response.status_code)+", header: "+str(login_post_response.headers)+")")
            else:
                response_header = login_post_response.headers
                #Extracting BearerToken from Responses Header
                self.bearer_token = (response_header["set-cookie"]).split(";")[0].replace("jwt=", "")
                if len(self.bearer_token) > 12:
                    token = (self.bearer_token)[0:461] + "=="
                    decoded_token =  base64.b64decode(token)
                    decoded_token_json = json.loads(decoded_token.decode('utf-8')[30:])
                    self.user_id = decoded_token_json["userId"]
                    self.school_id = decoded_token_json["schoolId"]
    return self

def logout(self):
    '''
    Starts the clean-up task after stopping the loadtest and logs out the user(s) afterwards.
    '''

    cleanUpLoadtest(self)
    self.client.get("/logout/", allow_redirects=True)
    self.csrf_token = None

def cleanUpLoadtest(self):
    '''
    Deletes all remaining documents, courses and teams which were created through the loadtest and keeps the stageing-test-area clean.
    Skips if no document-, course- our team- ID found.
    '''

    if self._user.user_type == "teacher":

        for documentId in self.createdDocuments :
            url = f"{self.user.host}/files/my/"
            with self.client.get(url, catch_response=True, allow_redirects=True) as response:
                soup = BeautifulSoup(response.text, "html.parser")
                findId = soup.find_all("div", {"data-file-id" : documentId}) # Searches document id on html page

            if len(findId) > 0:
                deleteDoc(self, documentId)
        self.createdDocuments = None

        for courseId in self.createdCourses:
            url = f"{self.user.host}/courses/"
            with self.client.get(url, catch_response=True, allow_redirects=True) as response:
                soup = BeautifulSoup(response.text, "html.parser")
                findId = soup.find_all("div", {"data-id" : courseId}) # Searches course id on html page
            if len(findId) > 0:
                deleteCourse(self, courseId)
        self.createdCourses = None

        for teamId in self.createdTeams:
            url = f"{self.user.host}/teams/"
            with self.client.get(url, catch_response=True, allow_redirects=True) as response:
                soup = BeautifulSoup(response.text, "html.parser")
                findId = soup.find_all({"data-id":teamId})
            if not findId is None:
                deleteTeam(self, teamId)
        self.createdTeams = None

def installChromedriver(self):
    self.workpath = str(os.path.dirname(os.path.abspath(__file__)))
    remote_url = 'https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip'
    # Define the local filename to save data
    local_file = self.workpath + '/chromedriver_linux64.zip'
    # Download remote and save locally
    urllib.request.urlretrieve(remote_url, local_file)
    os.chmod(local_file, stat.S_IRWXU)
    with zipfile.ZipFile(local_file,"r") as zip_ref:
        zip_ref.extractall(self.workpath)
    os.chmod(self.workpath + "/chromedriver", stat.S_IRWXU)

def deleteChromedriver(self):
    if os.path.exists(self.workpath + "/chromedriver"):
        os.remove(self.workpath + "/chromedriver")
    if os.path.exists(self.workpath + "/chromedriver_linux64.zip"):
        os.remove(self.workpath + "/chromedriver_linux64.zip")