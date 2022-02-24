import base64
import os
import json
import urllib.request
import stat
import zipfile

from bs4 import BeautifulSoup

from loadtests.shared.constant import Constant
from loadtests.loadtests.functions import *


def login(taskset):
    '''
    First task. Gets csrf token from login html website and logs in.
    Gets bearer token after login from the response header and extracts specific informations for further progress.
    '''

    with taskset.client.get("/login/", catch_response=True) as login_get_response:
        soup = BeautifulSoup(login_get_response.text, "html.parser")
        taskset.csrf_token = soup.select_one('meta[name="csrfToken"]')['content']

        login_data = {
            "challenge" : "",
            "username"  : taskset.user.login_credentials["email"],
            "password"  : taskset.user.login_credentials["password"],
            "_csrf"     : taskset.csrf_token
        }
        with taskset.client.request("POST", "/login/", data=login_data, catch_response=True, allow_redirects=False)  as login_post_response:
            if (login_post_response.status_code != Constant.returncodeRedirect) or not login_post_response.headers.get('location').startswith("/login/success"):
                login_post_response.failure("Failed! (username: " + taskset.user.login_credentials["email"] + ", http-code: "+str(login_post_response.status_code)+", header: "+str(login_post_response.headers)+")")
            else:
                response_header = login_post_response.headers
                #Extracting BearerToken from Responses Header
                taskset.bearer_token = (response_header["set-cookie"]).split(";")[0].replace("jwt=", "")
                if len(taskset.bearer_token) > 12:
                    token = (taskset.bearer_token)[0:461] + "=="
                    decoded_token =  base64.b64decode(token)
                    decoded_token_json = json.loads(decoded_token.decode('utf-8')[30:])
                    taskset.user_id = decoded_token_json["userId"]
                    taskset.school_id = decoded_token_json["schoolId"]
    return taskset

def logout(taskset):
    '''
    Starts the clean-up task after stopping the loadtest and logs out the user(s) afterwards.
    '''

    cleanUpLoadtest(taskset)
    taskset.client.get("/logout/", allow_redirects=True)
    taskset.csrf_token = None

def cleanUpLoadtest(taskset):
    '''
    Deletes all remaining documents, courses and teams which were created through the loadtest and keeps the stageing-test-area clean.
    Skips if no document-, course- our team- ID found.
    '''

    if taskset._user.user_type in ("teacher", "admin"):

        for documentId in taskset.createdDocuments :
            url = f"{taskset.user.host}/files/my/"
            with taskset.client.get(url, catch_response=True, allow_redirects=True) as response:
                soup = BeautifulSoup(response.text, "html.parser")
                findId = soup.find_all("div", {"data-file-id" : documentId}) # Searches document id on html page

            if len(findId) > 0:
                deleteDoc(taskset, documentId)
        taskset.createdDocuments = None

        for courseId in taskset.createdCourses:
            url = f"{taskset.user.host}/courses/"
            with taskset.client.get(url, catch_response=True, allow_redirects=True) as response:
                soup = BeautifulSoup(response.text, "html.parser")
                findId = soup.find_all("div", {"data-id" : courseId}) # Searches course id on html page
            if len(findId) > 0:
                deleteCourse(taskset, courseId)
        taskset.createdCourses = None

        for teamId in taskset.createdTeams:
            url = f"{taskset.user.host}/teams/"
            with taskset.client.get(url, catch_response=True, allow_redirects=True) as response:
                soup = BeautifulSoup(response.text, "html.parser")
                findId = soup.find_all({"data-id":teamId})
            if not findId is None:
                deleteTeam(taskset, teamId)
        taskset.createdTeams = None

def installChromedriver(taskset):
    taskset.workpath = str(os.path.dirname(os.path.abspath(__file__)))
    remote_url = 'https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip'
    # Define the local filename to save data
    local_file = taskset.workpath + '/chromedriver_linux64.zip'
    # Download remote and save locally
    urllib.request.urlretrieve(remote_url, local_file)
    os.chmod(local_file, stat.S_IRWXU)
    with zipfile.ZipFile(local_file,"r") as zip_ref:
        zip_ref.extractall(taskset.workpath)
    os.chmod(taskset.workpath + "/chromedriver", stat.S_IRWXU)

def deleteChromedriver(taskset):
    if os.path.exists(taskset.workpath + "/chromedriver"):
        os.remove(taskset.workpath + "/chromedriver")
    if os.path.exists(taskset.workpath + "/chromedriver_linux64.zip"):
        os.remove(taskset.workpath + "/chromedriver_linux64.zip")
