import json
import logging
import os
import random
import sys
import yaml
import time
import webbrowser
import hashlib

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException, NoSuchWindowException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from locust import HttpUser, TaskSet, between, task
from locust.exception import LocustError, CatchResponseError, ResponseError
from urllib.parse import urlparse

def is_static_file(f):
    if f.endswith(".css") or f.endswith(".png"):
        return True
    else:
        return False

def fetch_static_assets(session, response):
    resource_urls = set()
    soup = BeautifulSoup(response.text, "html.parser")

    for src in soup.find_all(src=True):
        url = src['src']
        if url.endswith(".js"):
            resource_urls.add(url)
 
    for res in soup.find_all(href=True):
        url = res['href']
        if is_static_file(url):
            resource_urls.add(url)    
    
    for use_url in resource_urls:
        with session.client.get(use_url, catch_response=True, allow_redirects=True) as response:
            if response.status_code != 200:
                    response.failure("Failed! (username: " + session.user.login_credentials["email"] + ", http-code: "+str(response.status_code)+", header: "+str(response.headers)+ ")")

def normalGET(session, url):
    with session.client.get(url, catch_response=True, allow_redirects=True) as response:
            if response.status_code != 200:
                response.failure("Failed! (username: " + session.user.login_credentials["email"] + ", http-code: "+str(response.status_code)+", header: "+str(response.headers)+ ")")
            else:
                fetch_static_assets(session, response)

def createDoc(session, docdata):
    with session.client.request(   
        "POST",
        "/files/newFile",
        headers = { 
            "Connection"        : "keep-alive",
            "x-requested-with"  : "XMLHttpRequest",
            "csrf-token"        : session.csrf_token,
            "Content-Type"      : "application/x-www-form-urlencoded",
            "Origin"            : "https://staging.niedersachsen.hpi-schul-cloud.org",
            "Sec-Fetch-Site"    : "same-origin",
            "Sec-Fetch-Mode"    : "cors",
            "Sec-Fetch-Dest"    : "empty",
            "Referer"           : "https://staging.niedersachsen.hpi-schul-cloud.org/files/my/"
        },
        data = docdata,
        catch_response = True, 
        allow_redirects = True
    ) as response:
        if response.status_code != 200:
            response.failure("Failed! (username: " + session.user.login_credentials["email"] + ", http-code: "+str(response.status_code)+", header: "+str(response.headers)+ ")")
        else:
            return response.text
            

def deleteDoc(session, docId):
    data = {
        "id" : docId
    }
    with session.client.request(
        "DELETE",
        "/files/file/",
        headers = {
            "Connection"        : "keep-alive",
            "x-requested-with"  : "XMLHttpRequest",
            "csrf-token"        : session.csrf_token,
            "Origin"            : "https://staging.niedersachsen.hpi-schul-cloud.org",
            "Sec-Fetch-Site"    : "same-origin",
            "Sec-Fetch-Mode"    : "cors",
            "Sec-Fetch-Dest"    : "empty",
            "Referer"           : "https://staging.niedersachsen.hpi-schul-cloud.org/files/my/"
        },
        data = data,
        catch_response = True, 
        allow_redirects = True
    ) as response:
        if response.status_code != 200:
            response.failure("Failed! (username: " + session.user.login_credentials["email"] + ", http-code: "+str(response.status_code)+", header: "+str(response.headers)+ ")")


class WebsiteTasks(TaskSet):
    next_batch = ""
    filter_id = None
    csrf_token = None
    token = None
    user_id = None
    room_ids = []
    
    def on_start(self):
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
                if (login_post_response.status_code != 302) or not login_post_response.headers.get('location').startswith("/login/success"):
                    login_post_response.failure("Failed! (username: " + self.user.login_credentials["email"] + ", http-code: "+str(login_post_response.status_code)+", header: "+str(login_post_response.headers)+")")
                else:
                    with self.client.request("GET", "/messenger/token", catch_response=True, allow_redirects=False) as response:
                        if(response.status_code == 200):
                            i = json.loads(response.text)
                            self.token = i["accessToken"]
                            self.user_id = i["userId"]
                    with self.client.get("/courses/" , catch_response=True, allow_redirects=True) as response:
                        if(response.status_code == 200):
                            soup = BeautifulSoup(response.text, "html.parser")
                            for room_id in soup.find_all('article'):
                                self.room_ids.append(room_id.get('data-loclink').removeprefix("/courses/"))

    def on_stop(self):
        self.client.get("/logout/", allow_redirects=True)
        self.csrf_token = None

    @task
    def index(self):
        self.client.get("/")

    @task
    def calendar(self):
        normalGET(self, "/calendar/")

    @task
    def account(self):
        normalGET(self, "/account/")

    @task
    def dashboard(self):
        normalGET(self, "/dashboard/")

    @task
    def courses(self):
        normalGET(self, "/courses/")

    @task
    def courses_add(self):
        normalGET(self, "/courses/add/")
    
    @task
    def homework(self):
        normalGET(self, "/homework/")

    @task
    def homework_new(self):
        normalGET(self, "/homework/new/")
        
    @task
    def homework_asked(self):
        normalGET(self, "/homework/asked/")

    @task
    def homework_private(self):
        normalGET(self, "/homework/private/")

    @task
    def homework_archive(self):
        normalGET(self, "/homework/archive/")

    @task
    def files(self):
        normalGET(self, "/files/")

    @task
    def files_my(self):
        normalGET(self, "/files/my/")

    @task
    def files_courses(self):
        normalGET(self, "/files/courses/")

    @task
    def files_shared(self):
        normalGET(self, "/files/shared/")

    @task
    def files_shared(self):
        normalGET(self, "/files/shared/")

    @task
    def news(self):
        normalGET(self, "/news/")

    @task
    def newsnew(self):
        normalGET(self, "/news/new")

    @task
    def addons(self):
        normalGET(self, "/addons/")

    @task
    def content(self):
        normalGET(self, "/content/")

    @task
    def courses_add_course(self):
        if "schueler" not in str(self.user.login_credentials["email"]):
            course_data = {
                "stage"     :"on",
                "_method"   :"post",
                "schoolId"  :"5f2987e020834114b8efd6f8",
                "name"      :"Loadtest",
                "color"     :"#ACACAC",
                "teacherIds":"0000d231816abba584714c9e",
                "startDate" :"01.08.2020",
                "untilDate" :"31.07.2021",
                "_csrf"     : self.csrf_token
            }
            with self.client.request("POST", "/courses/", data=course_data, catch_response=True, allow_redirects=True) as response:
                soup = BeautifulSoup(response.text, "html.parser")
                if response.status_code != 200:
                    response.failure("Failed! (username: " + self.user.login_credentials["email"] + ", http-code: "+str(response.status_code)+", header: "+str(response.headers)+ ")")
                else:
                    json_object = json.loads(soup.string)
                    with self.client.request("DELETE", 
                        "/courses/" + json_object["createdCourse"]["id"] + "/" , 
                        catch_response=True, 
                        allow_redirects=True, 
                        headers = {
                            "accept"            : "*/*",
                            "accept-language"   : "en-US,en;q=0.9",
                            "csrf-token"        : self.csrf_token,
                            "sec-fetch-dest"    : "empty",
                            "sec-fetch-mode"    : "cors",
                            "sec-fetch-site"    : "same-origin",
                            "x-requested-with"  : "XMLHttpRequest",
                            "referrer"          : ("https://staging.niedersachsen.hpi-schul-cloud.org/courses/"+ json_object["createdCourse"]["id"] +"/edit"),
                            "Origin"            : "https://staging.niedersachsen.hpi-schul-cloud.org"
                        }
                    ) as response:

                        if response.status_code != 200:
                            response.failure("Failed! (username: " + self.user.login_credentials["email"] + ", http-code: "+str(response.status_code)+", header: "+str(response.headers)+ ")")

    
    @task
    def message(self):
        txn_id = 0

        if "schueler" not in str(self.user.login_credentials["email"]):
            self.client.headers["authorization"] = "Bearer " + str(self.token)
            self.client.headers["accept"] = "application/json"

            payload = {
                "timeout": 30000
            }

            name = "https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/sync"
            response = self.client.get("https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/sync", params=payload)#, name=name)
            if response.status_code != 200:
                return

            json_response_dict = response.json()
            if 'next_batch' in json_response_dict:
                self.next_batch = json_response_dict['next_batch']


            # extract rooms
            if 'rooms' in json_response_dict and 'join' in json_response_dict['rooms']:
                room_ids = list(json_response_dict['rooms']['join'].keys())
                if len(room_ids) > 0:
                    self.room_ids = room_ids

            for room_id in self.room_ids:
                message = {
                    "msgtype"   : "m.text",
                    "body"      : "Load Test Message",
                }
                        
                self.client.put(
                    "https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/" + room_id + "/typing/" + self.user_id,
                    json={"typing": True, "timeout":30000},
                    #name="https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/" + room_id + "/typing/" + self.user_id + " - true"
                )

                self.client.put(
                    "https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/" + room_id + "/typing/" + self.user_id,
                    json={"typing": False},
                    #name="https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/" + room_id + "/typing/" + self.user_id + " - false"
                )

                with self.client.post(
                    "https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/" + room_id + "/send/m.room.message",
                    json=message,
                    #name="https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/" + room_id + "/send/m.room.message"
                ) as response:
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        json_object = json.loads(soup.string)
                        
                        data = {
                            "m.new_content" :{
                                "msgtype"   : "m.text",
                                "body"      : "Load Test !"
                            },
                            "m.relates_to"  :{
                                "rel_type"  : "m.replace",
                                "event_id"  : json_object['event_id']
                            },
                            "msgtype"       : "m.text",
                            "body"          : " * Load Test !"
                        }
                        self.client.post(
                            "https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/" + room_id + "/send/m.room.message",
                            json=data,
                            #name="https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/" + room_id + "/send/m.room.message"
                        )# as response
                            #soup = BeautifulSoup(response.text, "html.parser")
                            #json_object = json.loads(soup.string)
                            
                            #content = {
                            #    "reason" : "Loadtest"
                            #}
                            #params = None
                            #path = 'https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/rooms/%s/redact/%s/%s.1' % (
                            #    room_id, json_object['event_id'], txn_id
                            #)

                            #txn_id = txn_id + 1

                            #with self.client.put(path, 
                            #    HTTP/1.1,
                            #    headers = {
                            #        "Content-Type" : "application/json"
                            #    },
                            #    content) as response:
                            #    print(response)
                            

            self.client.get("https://matrix.niedersachsen.messenger.schule/_matrix/client/versions")

            self.client.get("https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/voip/turnServer")

            self.client.get("https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/pushrules/")

            self.client.get("https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/joined_groups")

            self.client.get(
                "https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/profile/" + self.user_id,
                #name="https://matrix.niedersachsen.messenger.schule/_matrix/client/r0/profile/" + self.user_id
            )
    

    @task
    def bBBTest(self):
        numberRooms = 3
        numberUsers = 6
        host = "https://bbb-1.bbb.staging.messenger.schule"
        filename = "./SHAREDS.txt"
        if not os.path.exists(filename):
            logger.error("File does not exist: " + filename)
            sys.exit(1)

        driverWB = webdriver.Chrome('.\chromedriver.exe')
        driverWB.get(host)

        shareds = open(filename, 'r').read()
        counterfirst = 0
        counterTab = 1
        while counterfirst < numberRooms:
            
            timestamp = str(time.time())

            v = "create"
            x = "meetingID=loadtest-" + timestamp + str(counterfirst) + "&name=loadtest-" + str(time.time()) + str(counterfirst) + "&moderatorPW=123&attendeePW=456&lockSettingsDisableMic=true"
            y = host + "/bigbluebutton/api/" + v + "?" + x
            z = str(v) + str(x) + str(shareds)
            w = str(y) + "&checksum=" + hashlib.sha1(z.encode()).hexdigest()

            driverWB.get(w)

            countersecond = 0

            v = "join"
            x = "meetingID=loadtest-" + timestamp + str(counterfirst) + "&fullName=loadtest-" + str(counterfirst) + "userMLoadtest-" + str(countersecond) + "&userID=loadtest-" + str(counterfirst) + "userMLoadtest-" + str(countersecond) + "&password=123"
            y = host + "/bigbluebutton/api/" + v + "?" + x
            z = str(v) + str(x) + str(shareds)
            w = y + "&checksum=" + hashlib.sha1(z.encode()).hexdigest()
                
            windows = driverWB.window_handles
            driverWB.execute_script("window.open('');")
            driverWB.switch_to.window(driverWB.window_handles[counterTab])
            driverWB.get(w)

            ui_element = "button[aria-label='Listen only']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(5)
            
            ui_element = "tippy-21"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.ID, ui_element)))
            element.click()

            ui_element = "li[aria-labelledby='dropdown-item-label-26']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            ui_element = "input[id='video-modal-input']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            #element.clear()
            element.send_keys('https://player.vimeo.com/video/418854539')

            time.sleep(2)

            ui_element = "button[aria-label='Share a new video']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(10) 

            counterTab += 1
            countersecond += 1
            
            while countersecond < numberUsers:
                
                v = "join"
                x = "meetingID=loadtest-" + timestamp + str(counterfirst) + "&fullName=loadtest-" + str(counterfirst) + "userLoadtest-" + str(countersecond) + "&userID=loadtest-" + str(counterfirst) + "userLoadtest-" + str(countersecond) + "&password=456"
                y = host + "/bigbluebutton/api/" + v + "?" + x
                z = str(v) + str(x) + str(shareds)
                w = y + "&checksum=" + hashlib.sha1(z.encode()).hexdigest()
                
                windows = driverWB.window_handles
                driverWB.execute_script("window.open('');")
                driverWB.switch_to.window(driverWB.window_handles[counterTab])
                driverWB.get(w)
                
                ui_element = "button[aria-label='Play audio']"
                element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
                element.click()

                time.sleep(10) 

                #ui_element = "button[class='play rounded-box state-paused']"
                #element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
                #element.click()

                countersecond += 1
                counterTab += 1

            counterfirst += 1
    
        counterfirst = 0
        time.sleep(30)
        while counterfirst < numberRooms:
            
            v = "end"
            x = "meetingID=loadtest-" + timestamp + str(counterfirst) + "&password=123"
            y = host + "/bigbluebutton/api/" + v + "?" + x
            z = str(v) + str(x) + str(shareds)
            w = str(y) + "&checksum=" + hashlib.sha1(z.encode()).hexdigest()
            
            driverWB.get(w)

            driverWB.quit()
            time.sleep(3)
            counterfirst += 1

    @task
    def newFilesDocx(self):
        if "schueler" not in str(self.user.login_credentials["email"]):
            data = {
                "name"          : "Loadtest docx",
                "type"          : "docx",
                "studentEdit"   : "false"
            }
            docId = createDoc(self, data)
            deleteDoc(self, docId)
            

    @task
    def newFilesXlsx(self):
        if "schueler" not in str(self.user.login_credentials["email"]):
            data = {
                "name"          : "Loadtest xlsx",
                "type"          : "xlsx",
                "studentEdit"   : "false"
            }
            docId = createDoc(self, data)
            deleteDoc(self, docId)
            
    @task
    def newFilesPptx(self):
        if "schueler" not in str(self.user.login_credentials["email"]):
            data = {
                "name"          : "Loadtest pptx",
                "type"          : "pptx",
                "studentEdit"   : "false"
            }
            docId = createDoc(self, data)
            deleteDoc(self, docId)

class AdminUser(HttpUser):
    weight = 1
    tasks = [WebsiteTasks]
    wait_time = between(5, 15)

    txn_id = ""
    user_type = "admin"
    next_batch = ""
    filter_id = None
    login_credentials = None

    def __init__(self, *args, **kwargs):
        super(AdminUser, self).__init__(*args, **kwargs)

        logger = logging.getLogger(__name__)

        hostname = urlparse(self.host).hostname
        filename = "./users_" + hostname + ".yaml"
        if not os.path.exists(filename):
            logger.error("File does not exist: " + filename)
            sys.exit(1)

        with open(filename, 'r') as file:
            yaml_loaded = yaml.safe_load(file)
            if (yaml_loaded != None) and (self.user_type in yaml_loaded):
                self.login_credentials = random.choice(yaml_loaded[self.user_type])

        if self.login_credentials == None:
            logger.info("No %s users found in " + filename, self.user_type)

class TeacherUser(HttpUser):
    weight = 3
    tasks = [WebsiteTasks]
    wait_time = between(5, 15)

    txn_id = ""
    user_type = "teacher"
    next_batch = ""
    filter_id = None
    login_credentials = None

    def __init__(self, *args, **kwargs):
        super(TeacherUser, self).__init__(*args, **kwargs)

        logger = logging.getLogger(__name__)

        hostname = urlparse(self.host).hostname
        filename = "./users_" + hostname + ".yaml"
        if not os.path.exists(filename):
            logger.error("File does not exist: " + filename)
            sys.exit(1)

        with open(filename, 'r') as file:
            yaml_loaded = yaml.safe_load(file)
            if (yaml_loaded != None) and (self.user_type in yaml_loaded):
                self.login_credentials = random.choice(yaml_loaded[self.user_type])

        if self.login_credentials == None:
            logger.info("No %s users found in " + filename, self.user_type)

class PupilUser(HttpUser):
    weight = 5
    tasks = [WebsiteTasks]
    wait_time = between(5, 15)

    txn_id = ""
    user_type = "pupil"
    next_batch = ""
    filter_id = None
    login_credentials = None

    def __init__(self, *args, **kwargs):
        super(PupilUser, self).__init__(*args, **kwargs)

        logger = logging.getLogger(__name__)

        hostname = urlparse(self.host).hostname
        filename = "./users_" + hostname + ".yaml"
        if not os.path.exists(filename):
            logger.error("File does not exist: " + filename)
            sys.exit(1)

        with open(filename, 'r') as file:
            yaml_loaded = yaml.safe_load(file)
            if (yaml_loaded != None) and (self.user_type in yaml_loaded):
                self.login_credentials = random.choice(yaml_loaded[self.user_type])

        if self.login_credentials == None:
            logger.info("No %s users found in " + filename, self.user_type)