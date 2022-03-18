
import json
import time

from bs4 import BeautifulSoup
from locust import task
from locust.user.task import tag

from loadtests.loadtests.config import Config
from loadtests.loadtests.chromedriver_download import asure_chromedriver
from loadtests.loadtests.constant import StatusCode
from loadtests.loadtests.taskset_base import TasksetBase
from loadtests.loadtests.user_type import UserType


asure_chromedriver()


class TasksetSchulCloud(TasksetBase):
    """
    Definition of the specific tasks, the loadtest should execute.
    Tasks, which are marked with tags, can be directly addressed by the start of the loadtest. The other tasks then will be ignored.
    """

    @tag('sc')
    @task
    def index(self):
        self.normal_get("/")

    @tag('sc')
    @task
    def calendar(self):
        self.normal_get("/calendar/")

    @tag('sc')
    @task
    def account(self):
        self.normal_get("/account/")

    @tag('sc')
    @task
    def dashboard(self):
        self.normal_get("/dashboard/")

    @tag('sc')
    @task
    def courses(self):
        self.normal_get("/courses/")

    @tag('sc')
    @task
    def courses_add(self):
        if not self.user.type == UserType.PUPIL:
            self.normal_get("/courses/add/")

    @tag('sc')
    @task
    def homework(self):
        self.normal_get("/homework/")

    @tag('sc')
    @task
    def homework_new(self):
        self.normal_get("/homework/new/")

    @tag('sc')
    @task
    def homework_asked(self):
        self.normal_get("/homework/asked/")

    @tag('sc')
    @task
    def homework_private(self):
        self.normal_get("/homework/private/")

    @tag('sc')
    @task
    def homework_archive(self):
        self.normal_get("/homework/archive/")

    @tag('sc')
    @task
    def files(self):
        self.normal_get("/files/")

    @tag('sc')
    @task
    def files_my(self):
        self.normal_get("/files/my/")

    @tag('sc')
    @task
    def files_courses(self):
        self.normal_get("/files/courses/")

    @tag('sc')
    @task
    def files_shared(self):
        self.normal_get("/files/shared/")

    @tag('sc')
    @task
    def files_shared(self):
        self.normal_get("/files/shared/")

    @tag('sc')
    @task
    def news(self):
        self.normal_get("/news/")

    @tag('sc')
    @task
    def newsnew(self):
        self.normal_get("/news/new")

    @tag('sc')
    @task
    def addons(self):
        self.normal_get("/addons/")

    @tag('sc')
    @task
    def content(self):
        self.normal_get("/content/")

    @tag('sc')
    @tag('course')
    @task
    def courses_add_lernstore(self):
        if not self.user.type == UserType.PUPIL:
            course_id = self.create_course(self.course_data_builder())
            if course_id:
                self.lernstore(course_id)
                self.delete_course(course_id)

    @tag('test')
    @tag('sc')
    @tag('course')
    @task
    def create_delete_course(self):
        if not self.user.type == UserType.PUPIL:
            course_id = self.create_course(self.course_data_builder())
            if course_id:
                #self.add_course_etherpad_and_tool(course_id)  # TODO: re-enable when fixed
                self.delete_course(course_id)

    @tag('sc')
    @task
    def create_delete_team(self):
        if not self.user.type == UserType.PUPIL:
            team_id = self.create_team()
            if team_id:
                self.delete_team(team_id)

    def message(self):
        # Posts and edits messages at the Matrix Messenger
        if not self.user.type == UserType.PUPIL:
            self.matrix_messanger()

    def lernstore(self, course_id):
        """
        Adds a theme.
        After that the id of the course is requestet from the lernstore to add Material of the Lernstore.

        Param:
            self: Taskset
        """

        # Add Resources
        if self.user.type == UserType.TEACHER:
            thema_data = self.thema_data_builder(course_id, "resources")

            # Adding a theme to the course to be able to add material from the Lernstore
            response = self.client.request("POST",
                                           f"/courses/{course_id}/topics",
                                           name="/courses/topics",
                                           data=thema_data,
                                           catch_response=True,
                                           allow_redirects=False)
            if response.status_code != StatusCode.OK:
                response.failure(self.request_failure_message(response))

            # Request to the Lernstore to get the internal id of the course
            headers = {
                "authority": "staging.niedersachsen.hpi-schul-cloud.org",
                "accept": "application/json, text/plain, */*",
                "authorization": f"Bearer {self.user.bearer_token}",
                "origin": self.user.host,
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty"
            }
            response = self.client.request("GET",
                                           f"{self.user.host}/api/v1/lessons?courseId={course_id}",
                                           name="/lessons?courseId=",
                                           data="courseId=" + course_id,
                                           catch_response=True,
                                           allow_redirects=False,
                                           headers=headers)
            if len(response.text) > 30:
                datajson = json.loads(response.text)
                datajson = json.dumps(datajson["data"])
                datajson = datajson[1:]
                datajson = datajson[:(len(datajson) - 1)]
                datajson = json.loads(datajson)
                course_id_lernstore = datajson["_id"]

                data = {
                    "title": "Geschichte der Mathematik - Die Sprache des Universums",
                    "client": "Schul-Cloud",
                    "url": "http://merlin.nibis.de/auth.php?identifier=BWS-04983086",
                    "merlinReference": "BWS-04983086"
                }

                # Adding a material from the Lernstore to the course
                headers = {
                    "authority": "staging.niedersachsen.hpi-schul-cloud.org",
                    "path": f"/lessons/{course_id_lernstore}/material",
                    "scheme": "https",
                    "accept": "application/json, text/plain, */*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "authorization": f"Bearer {self.user.bearer_token}",
                    "content-type": "application/json;charset=UTF-8",
                    "origin": self.user.host,
                    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "sec-ch-ua-moblie": "?0"
                }
                response = self.client.request("POST",
                                               f"{self.user.host}/api/v1/lessons/{course_id_lernstore}/material",
                                               data=json.dumps(data),
                                               name="/lessons/material",
                                               catch_response=True,
                                               allow_redirects=False,
                                               headers=headers)
                if response.status_code != StatusCode.CREATED:
                    response.failure(self.request_failure_message(response))

    def add_course_etherpad_and_tool(self, course_id):

        # TODO: get bettermarks url

        bettermarks_url = None

        raise NotImplementedError()

        # Add Etherpads
        if self.user.type == UserType.TEACHER:
            thema_data = self.thema_data_builder(course_id, "Etherpad")
            thema_data["contents[0][content][title]"] = ""
            thema_data["contents[0][content][description]"] = ""
            thema_data["contents[0][content][url]"] = f"{self.user.host}/etherpad/pi68ca"

            response = self.client.request("POST",
                                           f"/courses/{course_id}/topics",
                                           name="/courses/topics",
                                           data=thema_data,
                                           catch_response=True,
                                           allow_redirects=False)
            if response.status_code != StatusCode.OK:
                response.failure(self.request_failure_message(response))

            # Add Tool
            headers = {
                 "accept": "*/*",
                 "accept-language": "en-US,en;q=0.9",
                 "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                 "csrf-token": self.user.csrf_token,
                 "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                 "sec-ch-ua-mobile": "?0",
                 "sec-fetch-dest": "empty",
                 "sec-fetch-mode": "cors",
                 "sec-fetch-site": "same-origin",
                 "x-requested-with": "XMLHttpRequest"
            }
            body = f'privacy_permission=anonymous&openNewTab=true&name=bettermarks&url={bettermarks_url}'\
                   '&key=&logo_url=https://acc.bettermarks.com/app/assets/bm-logo.png'\
                   '&isLocal=true&resource_link_id=&lti_version=&lti_message_type=&isTemplate=false'\
                   '&skipConsent=false&createdAt=2021-01-14T13:35:44.689Z'\
                   '&updatedAt=2021-01-14T13:35:44.689Z&__v=0'\
                   f'&originTool=600048b0755565002840fde4&courseId={course_id}'
            self.client.request("POST",
                                f"/courses/{course_id}/tools/add",
                                name="/courses/tools/add",
                                headers=headers,
                                data=body.encode(),
                                catch_response=True,
                                allow_redirects=False)
            response = self.client.request("GET", str(bettermarks_url), catch_response=True, allow_redirects=False)
            if response.status_code != StatusCode.OK:
                response.failure(self.request_failure_message(response))

    def matrix_messanger(self):
        """
        Method is not used and not functional
        """

        txn_id = 0
        main_host = None  # TODO: get matrix messenger url
        raise NotImplementedError()

        with self.client.request("GET", "/messenger/token", catch_response=True, allow_redirects=False) as response:
            if response.status_code == StatusCode.OK:
                i = json.loads(response.text)
                token = i["accessToken"]
                user_id = i["userId"]

        room_ids = []
        with self.client.get("/courses/", catch_response=True, allow_redirects=False) as response:
            if response.status_code == StatusCode.OK:
                soup = BeautifulSoup(response.text, "html.parser")
                for room_id in soup.find_all('article'):
                    room_ids.append(room_id.get('data-loclink').removeprefix("/courses/"))

        self.client.headers["authorization"] = "Bearer " + str(token)
        self.client.headers["accept"] = "application/json"

        payload = {
            "timeout": 30000
        }

        name = f"{main_host}/r0/sync"
        response = self.client.get(f"{main_host}/r0/sync", params=payload)  # , name=name)
        if response.status_code != StatusCode.OK:
            return

        json_response_dict = response.json()
        if 'next_batch' in json_response_dict:
            next_batch = json_response_dict['next_batch']

        # extract rooms
        if 'rooms' in json_response_dict and 'join' in json_response_dict['rooms']:
            room_ids = list(json_response_dict['rooms']['join'].keys())
            if len(room_ids) > 0:
                room_ids = room_ids

        for room_id in room_ids:
            message = {
                "msgtype": "m.text",
                "body": "Load Test Message",
            }

            self.client.put(
                f"{main_host}/r0/rooms/{room_id}/typing/{user_id}",
                json={"typing": True, "timeout": 30000},
            )

            self.client.put(
                f"{main_host}/r0/rooms/{room_id}/typing/{user_id}",
                json={"typing": False},
            )

            response = self.client.post(f"{main_host}/r0/rooms/{room_id}/send/m.room.message", json=message)
            if response.status_code == StatusCode.OK:
                soup = BeautifulSoup(response.text, "html.parser")
                json_object = json.loads(soup.string)

                data = {
                    "m.new_content": {
                        "msgtype": "m.text",
                        "body": "Load Test !"
                    },
                    "m.relates_to": {
                        "rel_type": "m.replace",
                        "event_id": json_object['event_id']
                    },
                    "msgtype": "m.text",
                    "body": " * Load Test !"
                }
                self.client.post(f"{main_host}/r0/rooms/{room_id}/send/m.room.message", json=data)

        self.client.get(f"{main_host}/versions")

        self.client.get(f"{main_host}/r0/voip/turnServer")

        self.client.get(f"{main_host}/r0/pushrules/")

        self.client.get(f"{main_host}/r0/joined_groups")

        self.client.get(f"{main_host}/r0/profile/{user_id}")
