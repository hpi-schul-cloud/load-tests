
import json
import logging
import re
from typing import List

from bs4 import BeautifulSoup
from locust import TaskSet

from loadtests.loadtests.constant import StatusCode


logger = logging.getLogger(__name__)


class TasksetBase(TaskSet):

    # THIS TASKSET IS NOT ALLOWED TO HAVE ANY TASKS ITSELF!

    all_documents: List[str] = []
    all_courses: List[str] = []
    all_teams: List[str] = []

    def on_stop(self):
        if len(self.all_documents):
            logger.warning('Not all documents have been cleaned up')
            for doc in self.all_documents:
                self.delete_doc(doc)
        if len(self.all_courses):
            logger.warning('Not all courses have been cleaned up')
            for course in self.all_courses:
                self.delete_course(course)
        if len(self.all_teams):
            logger.warning('Not all teams have been cleaned up')
            for team in self.all_teams:
                self.delete_team(team)

    def create_doc(self, docdata):
        header = self.request_header_builder("/files/my/")
        header["Content-Type"] = "application/x-www-form-urlencoded"

        response = self.client.request(
            "POST",
            "/files/newFile",
            headers=header,
            data=docdata,
            catch_response=True,
            allow_redirects=False)
        if response.status_code != StatusCode.OK:
            response.failure(self.request_failure_message(response))
        else:
            self.all_documents.append(response.text)
            return response.text

    def delete_doc(self, doc_id):
        data = {"id": doc_id}
        response = self.client.request(
            "DELETE",
            "/files/file/",
            headers=self.request_header_builder("/files/my/"),
            data=data,
            catch_response=True,
            allow_redirects=False,
            name="/files/file/delete"
        )
        if response.status_code != StatusCode.OK:
            response.failure(self.request_failure_message(response))
        else:
            self.all_documents.remove(doc_id)

    def create_course(self, data):
        response = self.client.request("POST", "/courses/", data=data, catch_response=True, allow_redirects=False)
        soup = BeautifulSoup(response.text, "html.parser")
        if response.status_code != StatusCode.OK:
            response.failure(self.request_failure_message(response))
        else:
            try:
                json_object = json.loads(str(soup))
                course_id = str(json_object["createdCourse"]["id"])
                self.all_courses.append(course_id)
                return course_id
            except KeyError:
                raise RuntimeError('Answer has no course id')

    def delete_course(self, course_id):
        header = self.request_header_builder("/courses/" + course_id + "/edit")
        header["accept"] = "*/*"
        header["accept-language"] = "en-US,en;q=0.9"

        response = self.client.request("DELETE",
                                       f"/courses/{course_id}/",
                                       headers=header,
                                       catch_response=True,
                                       allow_redirects=False,
                                       name="/courses/delete")
        if response.status_code != StatusCode.OK:
            response.failure(self.request_failure_message(response))
        else:
            self.all_courses.remove(course_id)

    def create_team(self):

        team_id = None

        data = {
            "schoolId": self.user.school_id,
            "_method": "post",
            "name": "Loadtest Team",
            "description": "Loadtest Team",
            "rocketChat": "true",
            "color": "#d32f2f",
            "_csrf": self.user.csrf_token
        }

        # Creates a team
        with self.client.request(
            "POST",
            self.user.host + "/teams/",
            headers={
                "authority": self.user.host.replace("https://", ""),
                "path": "/teams/",
                "origin": self.user.host,
                "referer": f"{self.user.host}/teams/add"
            },
            data=data,
            catch_response=True,
            allow_redirects=False
        ) as response:
            if response.status_code != StatusCode.REDIRECT:
                response.failure(self.request_failure_message(response))
            else:
                team_id = re.search(r'/teams/([a-f0-9]*)', response.text).group(1)
                self.all_teams.append(team_id)

        return team_id

    def delete_team(self, team_id):

        header = self.request_header_builder(f"{str(self.user.host)}/teams/{team_id}/")
        header["accept"] = "*/*"
        header["accept-language"] = "en-US,en;q=0.9"

        response = self.client.request("DELETE",
                                       f"/teams/{team_id}/",
                                       headers=header,
                                       name="/teams/delete",
                                       catch_response=True,
                                       allow_redirects=False)
        # TODO: currently causes an internal server error while the real client works just fine
        if response.status_code != StatusCode.OK:
            response.failure(self.request_failure_message(response))
        else:
            self.all_teams.remove(team_id)

    def fetch_static_assets(self, response):
        """
        Scans the hmtl-page for Js and Css Files and requests the single urls/files after successful get-request.
        """

        resource_urls = set()
        soup = BeautifulSoup(response.text, "html.parser")

        for src in soup.find_all(src=True):
            url = src['src']
            if url.endswith(".js"):
                resource_urls.add(url)
            if url.endswith(".svg"):
                resource_urls.add(url)

            for font in soup.find_all(type="font/woff"):
                resource_urls.add(font['href'])

            for font in soup.find_all(type="font/woff2"):
                resource_urls.add(font['href'])

        for res in soup.find_all(href=True):
            url = res['href']
            if url.endswith(".css") or url.endswith(".png"):
                resource_urls.add(url)

        for use_url in resource_urls:
            if use_url != "/themes/n21/favicon.png":
                with self.client.get(use_url, catch_response=True, allow_redirects=True) as response:
                    if response.status_code != StatusCode.OK:
                        response.failure(self.request_failure_message(response))

    def request_failure_message(self, response):
        """
        Failure Message for unsuccessfull requests.
        """

        return f"Failed! (username: {self.user.credentials['email']}, http-code: {str(response.status_code)}, header: {str(response.headers)})"

    def normal_get(self, url):
        """
        Normal Get-Request for an URL
        """

        response = self.client.get(url, catch_response=True, allow_redirects=True)
        if response.status_code != StatusCode.OK:
            response.failure(self.request_failure_message(response))

    def request_header_builder(self, referer_url):
        """
        Builds the request header for the specific request within the provided session information.
        """

        header = {
            "Connection": "keep-alive",
            "x-requested-with": "XMLHttpRequest",  # Used for identifying Ajax requests
            "csrf-token": self.user.csrf_token,  # Security token
            "Origin": self.user.host,
            "Sec-Fetch-Site": "same-origin",  # Indicates the origin of the request
            "Sec-Fetch-Mode": "cors",  # Indicates the mode of the request
            "Sec-Fetch-Dest": "empty",  # Indicates the request's destination
            "Referer": self.user.host + referer_url
        }
        return header

    def course_data_builder(self):
        """
        Provides the create-course method with needed course informations.
        """

        course_data = {
            "stage": "on",
            "_method": "post",
            "schoolId": self.user.school_id,
            "name": "Loadtest Lernstore",
            "color": "#ACACAC",
            "teacherIds": self.user.user_id,
            "startDate": "01.08.2020",
            "untilDate": "31.07.2023",
            "times[0][weekday]": "0",
            "times[0][startTime]": "12:00",
            "times[0][duration]": "90",
            "times[0][room]": "1",
            "times[1][weekday]": "2",
            "times[1][startTime]": "12:00",
            "times[1][duration]": "90",
            "times[1][room]": "2",
            "_csrf": self.user.csrf_token
        }

        return course_data

    def thema_data_builder(self, course_id, component):
        """
        Provides necessary informations for adding a theme to the course, to be able to add material from the Lernstore.

        Param:
            self: Taskset
            courseId: Course ID
            components:
        """

        thema_data = {
            "authority": self.user.host.replace("https://", ""),
            "origin": self.user.host,
            "referer": f"{self.user.host}/courses/{course_id}/tools/add",
            "_method": "post",
            "position": "",
            "courseId": course_id,
            "name": "Test1",
            "contents[0][title]": "Test2",
            "contents[0][hidden]": "false",
            "contents[0][component]": component,
            "contents[0][user]": "",
            "_csrf": self.user.csrf_token
        }

        return thema_data
