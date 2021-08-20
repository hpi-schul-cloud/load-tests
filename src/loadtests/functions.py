import json
from random import betavariate
import requests
import time

from loadtests import requestsBuilder
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium import webdriver
from requests.api import head
from loadtests.requestsBuilder import *

def createDoc(self, docdata):
    '''
    Creates a document on the SchulCloud website.

    Param:
        self: Taskset
        docdata: Configuration for the new Document
    '''

    header = requestHeaderBuilder(self, "/files/my/")
    header["Content-Type"] = "application/x-www-form-urlencoded" # Adding entry "Content-Type" (data format for request body)

    with self.client.request(
        "POST",
        "/files/newFile",
        headers = header,
        data = docdata,
        catch_response = True,
        allow_redirects = True
    ) as response:
        if response.status_code != constant.constant.returncodeNormal:
            response.failure(requestFailureMessage(self, response))
        else:
            self.createdDocuments.append(response.text) # Adding the new document to createdDocumets-list for final clean-up
            return response.text

def deleteDoc(self, docId):
    '''
    Deletes a document on the SchulCloud website.

    Param:
        self: Taskset
        docId: Document ID
    '''

    data = {"id" : docId}
    with self.client.request(
        "DELETE",
        "/files/file/",
        headers = requestHeaderBuilder(self, "/files/my/"),
        data = data,
        catch_response = True,
        allow_redirects = True,
        name="/files/file/delete"
    ) as response:
        if response.status_code != constant.constant.returncodeNormal:
            response.failure(requestFailureMessage(self, response))

def createCourse(self, data):
    '''
    Creates a course

    Param:
        self: Taskset
        data: Configuration of the course
    '''

    with self.client.request("POST", "/courses/", data=data, catch_response=True, allow_redirects=True) as response:
        soup = BeautifulSoup(response.text, "html.parser")
        if response.status_code != constant.constant.returncodeNormal:
            response.failure(requestFailureMessage(self, response))
        else:
            json_object = json.loads(str(soup.string))
            courseId = str(json_object["createdCourse"]["id"])
            self.createdCourses.append(courseId)
            return (courseId)

def deleteCourse(self, courseId):
    '''
    Delete a course

    Param:
        self: Taskset
        data: Configuration of the course
    '''

    header = requestHeaderBuilder(self, "/courses/"+ courseId +"/edit")
    header["accept"] = "*/*" # Adding "accept" entry
    header["accept-language"] = "en-US,en;q=0.9" # Adding accepted language

    with self.client.request("DELETE",
        "/courses/" + courseId + "/" ,
        headers = header,
        catch_response=True,
        allow_redirects=True,
        name="/courses/delete"
    ) as response:
        if response.status_code != constant.constant.returncodeNormal:
            response.failure(requestFailureMessage(self, response))

def lernStore(self, courseId):
    '''
    Adds a theme.
    After that the id of the course is requestet from the lernstore to add Material of the Lernstore.

    Param:
        self: Taskset
    '''

    # Add Resources
    if self._user.user_type == "teacher":
        thema_data = themaDataBuilder(self, courseId, "resources")

        # Adding a theme to the course to be able to add material from the Lernstore
        with self.client.request("POST",
            "/courses/" + courseId + "/topics",
            name="/courses/topics",
            data=thema_data,
            catch_response=True,
            allow_redirects=True
        ) as response:
            if response.status_code != constant.constant.returncodeNormal:
                response.failure(requestFailureMessage(self, response))

            # Request to the Lernstore to get the internal id of the course
            with self.client.request("GET",
                "https://api." + self.user.host.replace("https://", "") + "/lessons?courseId=" + courseId,
                name="/lessons?courseId=",
                data="courseId=" + courseId,
                catch_response=True,
                allow_redirects=True,
                headers = {
                    "authority"         : "api.staging.niedersachsen.hpi-schul-cloud.org",
                    "accept"            : "application/json, text/plain, */*",
                    "authorization"     : "Bearer " + self.bearer_token,
                    "origin"            : self.user.host,
                    "sec-fetch-site"    : "same-site",
                    "sec-fetch-mode"    : "cors",
                    "sec-fetch-dest"    : "empty"
                }
            ) as response:

                datajson = json.loads(response.text)
                datajson = json.dumps(datajson["data"])
                datajson = json.loads(datajson.removeprefix("[").removesuffix("]"))
                courseId_Lernstore = datajson["_id"]

                data = {
                    "title":"Geschichte der Mathematik - Die Sprache des Universums",
                    "client":"Schul-Cloud",
                    "url":"http://merlin.nibis.de/auth.php?identifier=BWS-04983086",
                    "merlinReference":"BWS-04983086"
                }

                # Adding a material from the Lernstore to the course
                with self.client.request("POST",
                    "https://api." + self.user.host.replace("https://", "") + "/lessons/" + courseId_Lernstore + "/material",
                    data=json.dumps(data),
                    name="/lessons/material",
                    catch_response=True,
                    allow_redirects=True,
                    headers = {
                        "authority"         : "api.staging.niedersachsen.hpi-schul-cloud.org",
                        "path"  	        : "/lessons/" + courseId_Lernstore + "/material",
                        "scheme"            : "https",
                        "accept"            : "application/json, text/plain, */*",
                        "accept-encoding"   : "gzip, deflate, br",
                        "accept-language"   : "en-US,en;q=0.9",
                        "authorization"     : "Bearer " + self.bearer_token,
                        "content-type"      : "application/json;charset=UTF-8",
                        "origin"            : self.user.host,
                        "sec-ch-ua"         : '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                        "sec-ch-ua-moblie"  : "?0",
                        "sec-fetch-site"    : "same-site",
                        "sec-fetch-mode"    : "cors",
                        "sec-fetch-dest"    : "empty",
                        "sec-ch-ua-moblie"  : "?0"
                    }
                ) as response:
                    if response.status_code != constant.constant.returncodeCreated:
                        response.failure(requestFailureMessage(self, response))

def courseAddEtherPadAndTool(self, courseId):
    '''
    Creates and deletes a Course and adds an Etherpad and a Tool, if the User is an Teacher.
    If the User is an Admin, it only creates and deletes a Course

    Param:
        self: Taskset
    '''

    # Add Etherpads
    if self._user.user_type == "teacher":
        thema_data = themaDataBuilder(self, courseId, "Etherpad")
        thema_data["contents[0][content][title]"] = ""
        thema_data["contents[0][content][description]"] = ""
        thema_data["contents[0][content][url]"] = self.user.host + "/etherpad/pi68ca"

        with self.client.request("POST",
            "/courses/" + courseId + "/topics",
            name="/courses/topics",
            data=thema_data,
            catch_response=True,
            allow_redirects=True
        ) as response:
            if response.status_code != constant.constant.returncodeNormal:
                response.failure(requestFailureMessage(self, response))

        # Add Tool
        with self.client.request("POST",
            "/courses/" + str(courseId) + "/tools/add",
            name="/courses/tools/add",
            headers = {
                "accept"            : "*/*",
                "accept-language"   : "en-US,en;q=0.9",
                "content-type"      : "application/x-www-form-urlencoded; charset=UTF-8",
                "csrf-token"        : self.csrf_token,
                "sec-ch-ua"         : "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
                "sec-ch-ua-mobile"  : "?0",
                "sec-fetch-dest"    : "empty",
                "sec-fetch-mode"    : "cors",
                "sec-fetch-site"    : "same-origin",
                "x-requested-with"  : "XMLHttpRequest"
            },
            data = ("privacy_permission=anonymous&openNewTab=true&name=bettermarks&url="
                + constant.constant.urlBetterMarks +
                "&key=&logo_url=https://acc.bettermarks.com/app/assets/bm-logo.png&isLocal=true&resource_link_id=&lti_version=&lti_message_type=&isTemplate=false&skipConsent=false&createdAt=2021-01-14T13:35:44.689Z&updatedAt=2021-01-14T13:35:44.689Z&__v=0&originTool=600048b0755565002840fde4&courseId="
                + str(courseId)),
            catch_response=True,
            allow_redirects=True
        ) as response:
            with self.client.request("GET",
                constant.constant.urlBetterMarks,
                catch_response=True,
                allow_redirects=True
            ) as response:
                if response.status_code != constant.constant.returncodeNormal:
                    response.failure(requestFailureMessage(self, response))

def newTeam(self):
    '''
    Creates a new team

    Param:
        self: Taskset
    '''

    teamId = None

    data = {
        "schoolId"      : self.school_id,
        "_method"       : "post",
        "name"          : "Loadtest Team",
        "description"   : "Loadtest Team",
        "messenger"     : "true",
        "rocketChat"    : "true",
        "color"         : "#d32f2f",
        "_csrf"         : self.csrf_token
    }

    # Creates a team
    with self.client.request(
        "POST",
        self.user.host + "/teams/",
        headers = {
            "authority" : self.user.host.replace("https://", ""),
            "path"      : "/teams/",
            "origin"    : self.user.host,
            "referer"   : self.user.host + "/teams/add"
        },
        data = data,
        catch_response=True,
        allow_redirects=True
    ) as response:
        if response.status_code != constant.constant.returncodeNormal:
            response.failure(requestFailureMessage(self, response))
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            teamIdString = soup.find_all("section", {"class": "section-teams"})
            teamId = str(teamIdString).partition('\n')[0][41:65]
            self.createdTeams.append(teamId)

    return teamId

def deleteTeam(self, teamId):
    '''
    Deletes a team

    Param:
        self: Taskset
        teamId: Id of the team
    '''

    header = requestHeaderBuilder(self, (self.user.host + "/teams/" + teamId + "/edit"))
    header["accept"] = "*/*"
    header["accept-language"] = "en-US,en;q=0.9"

    with self.client.request("DELETE",
        "/teams/" + teamId + "/" ,
        headers = header,
        name="/teams/delete",
        catch_response=True,
        allow_redirects=True
    ) as response:
        if response.status_code != constant.constant.returncodeNormal:
            response.failure(requestFailureMessage(self, response))

def loginLoadtestUserOnTeamToEdit(self, webbrowser):
    '''
    Logs-in a user on the 'edit-page' of a team on SchulCloud.
    '''

    # Login user
    ui_element = "input[id='name']"
    element = WebDriverWait(webbrowser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
    element.send_keys(self.user.login_credentials["email"])

    ui_element = "input[id='password']"
    element = WebDriverWait(webbrowser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
    element.send_keys(self.user.login_credentials["password"])

    ui_element = "input[id='submit-login']"
    element = WebDriverWait(webbrowser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
    element.click()

    time.sleep(1)

def enableTeamMessenger(webbrowser):
    '''
    Enables the team-messenger. This will create a new chat on RocketChat. When the team will be deleted later,
    the connected rocket chat will be deleted as well. Only works with an already startet webbrowser, where the user is already logged in.
    '''

    # Klick on rocket chat checkbox
    ui_element = "input[id='activateRC']"
    element = WebDriverWait(webbrowser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
    element.click()
    time.sleep(1)

    # Apply changes
    ui_element = "button[data-testid='create_team_btn']"
    element = WebDriverWait(webbrowser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
    element.click()
    time.sleep(1)


def findTeamChatId(self, teamId):
    '''
    Returns the team-chat-id of the provided team.
    '''

    url = f"{self.user.host}/teams/{teamId}"

    # Get team-chat-id
    with self.client.request(
        "GET",
        url,
        headers = requestsBuilder.requestHeaderBuilder(self, self.user.host),
        catch_response = True,
        allow_redirects = True
    ) as response:
        if response.status_code == constant.constant.returncodeNormal:
            soup = BeautifulSoup(response.text, 'html.parser')
            teamChatId = soup.find('iframe')['src']
            host = self.user.host.replace("https://", "")
            return teamChatId.replace('?layout=embedded', '').replace(f"https://chat.{host}/group/", '')
        else:
            response.failure(requestFailureMessage(self, response))


def postTeamChatMessage(self, webbrowser):
    '''
    Posts a message on rocket chat.
    '''

    # Type in the test message
    ui_element = "textarea[class='rc-message-box__textarea js-input-message']"
    element = WebDriverWait(webbrowser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
    element.send_keys("This is an automated loadtest chat message.")

    # Klick 'send' button
    ui_element = "svg[class='rc-icon rc-input__icon-svg rc-input__icon-svg--send']"
    element = WebDriverWait(webbrowser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
    element.click()

    time.sleep(1)


def matrixMessenger(self):
    '''
    Method is not used and not functional
    '''
    txn_id = 0
    mainHost = constant.constant.MATRIX_MESSENGER
    with self.client.request("GET", "/messenger/token", catch_response=True, allow_redirects=False) as response:
                if(response.status_code == constant.constant.returncodeNormal):
                    i = json.loads(response.text)
                    self.token = i["accessToken"]
                    self.user_id = i["userId"]

    room_ids = None
    with self.client.get("/courses/" , catch_response=True, allow_redirects=True) as response:
        if(response.status_code == constant.constant.returncodeNormal):
            soup = BeautifulSoup(response.text, "html.parser")
            for room_id in soup.find_all('article'):
                room_ids.append(room_id.get('data-loclink').removeprefix("/courses/"))

    self.client.headers["authorization"] = "Bearer " + str(self.token)
    self.client.headers["accept"] = "application/json"

    payload = {
        "timeout": 30000
    }

    name = mainHost + "/r0/sync"
    response = self.client.get(mainHost + "/r0/sync", params=payload)#, name=name)
    if response.status_code != constant.constant.returncodeNormal:
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
            mainHost + "/r0/rooms/" + room_id + "/typing/" + self.user_id,
            json={"typing": True, "timeout":30000},
        )

        self.client.put(
            mainHost + "/r0/rooms/" + room_id + "/typing/" + self.user_id,
            json={"typing": False},
        )

        with self.client.post(
            mainHost + "/r0/rooms/" + room_id + "/send/m.room.message",
            json=message,
        ) as response:
            if response.status_code == constant.constant.returncodeNormal:
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
                    mainHost + "/r0/rooms/" + room_id + "/send/m.room.message",
                    json=data,
                )

    self.client.get(mainHost + "/versions")

    self.client.get(mainHost + "/r0/voip/turnServer")

    self.client.get(mainHost + "/r0/pushrules/")

    self.client.get(mainHost + "/r0/joined_groups")

    self.client.get(mainHost + "/r0/profile/" + self.user_id)
