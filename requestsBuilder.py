import json
import os
import locustfile

from bs4 import BeautifulSoup

def fetch_static_assets(self, response):
    '''
    Scans the hmtl-page for Js and Css Files and requests the single urls/files after successful get-request.
    '''

    resource_urls = set()
    soup = BeautifulSoup(response.text, "html.parser")

    for src in soup.find_all(src=True):
        url = src['src']
        if url.endswith(".js"):
            resource_urls.add(url)

    for res in soup.find_all(href=True):
        url = res['href']
        if f.endswith(".css") or f.endswith(".png"):
            resource_urls.add(url)

    for use_url in resource_urls:
        with self.client.get(use_url, catch_response=True, allow_redirects=True) as response:
            if response.status_code != self.returncode:
                    response.failure(requestFailureMessage(self, response))

def requestFailureMessage(self, response):
    '''
    Failure Message for unsuccessfull requests.
    '''

    return (f"Failed! (username: {self.user.login_credentials['email']}, http-code: {str(response.status_code)}, header: {str(response.headers)})")

def normalGET(self, url):
    '''
    Normal Get-Request for an URL
    '''

    with self.client.get(url, catch_response=True, allow_redirects=True) as response:
        if response.status_code != self.returncode:
            response.failure(requestFailureMessage(self, response))
        else:
            fetch_static_assets(self, response)

def requestHeaderBuilder(self, referer_url):
    '''
    Builds the request header for the specific request within the provided session information.
    '''

    header = {
        "Connection"        : "keep-alive", # 'keep-alive' allows the connection to remain open for further requests/response
        "x-requested-with"  : "XMLHttpRequest", # Used for identifying Ajax requests
        "csrf-token"        : self.csrf_token, # Security token
        "Origin"            : self.user.host,
        "Sec-Fetch-Site"    : "same-origin", # Indicates the origin of the request
        "Sec-Fetch-Mode"    : "cors", # Indicates the mode of the request
        "Sec-Fetch-Dest"    : "empty", # Indicates the request's destination
        "Referer"           : self.user.host + referer_url
    }
    return header

def courseDataBuilder(self):
    '''
    Provides the create-course method with needed course informations.
    '''

    course_data = {
        "stage"                 : "on",
        "_method"               : "post",
        "schoolId"              : self.school_id,
        "name"                  : "Loadtest Lernstore",
        "color"                 : "#ACACAC",
        "teacherIds"            : self.user_id,
        "startDate"             : "01.08.2020",
        "untilDate"             : "31.07.2022",
        "times[0][weekday]"     : "0",
        "times[0][startTime]"   : "12:00",
        "times[0][duration]"    : "90",
        "times[0][room]"        : "1",
        "times[1][weekday]"     : "2",
        "times[1][startTime]"   : "12:00",
        "times[1][duration]"    : "90",
        "times[1][room]"        : "2",
        "_csrf"                 : self.csrf_token
    }

    return course_data

def themaDataBuilder(self, courseId, component):
    '''
    Provides necessary informations for adding a theme to the course, to be able to add material from the Lernstore.
    '''
    
    thema_data = {
        "authority"                         : self.user.host.replace("https://", ""),
        "origin"                            : self.user.host,
        "referer"                           : self.user.host + "/courses/" + courseId + "/tools/add",
        "_method"                           : "post",
        "position"                          : "",
        "courseId"                          : courseId,
        "name"                              : "Test1",
        "contents[0][title]"                : "Test2",
        "contents[0][hidden]"               : "false",
        "contents[0][component]"            : component,
        "contents[0][user]"                 : "",
        "_csrf"                             : self.csrf_token
    }

    return thema_data

def createDoc(self, docdata):
    '''
    Creates a document on the SchulCloud website.
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
        if response.status_code != self.returncode:
            response.failure(requestFailureMessage(self, response))
        else:
            self.createdDocuments.append(response.text) # Adding the new document to createdDocumets-list for final clean-up
            return response.text

def deleteDoc(self, docId):
    '''
    Deletes a document on the SchulCloud website.
    '''

    data = {"id" : docId}
    print(docId)
    with self.client.request(
        "DELETE",
        "/files/file/",
        headers = requestHeaderBuilder(self, "/files/my/"),
        data = data,
        catch_response = True,
        allow_redirects = True,
        name="/files/file/delete"
    ) as response:
        if response.status_code != self.returncode:
            response.failure(requestFailureMessage(self, response))

def createCourse(self, data):
    with self.client.request("POST", "/courses/", data=data, catch_response=True, allow_redirects=True) as response:
        soup = BeautifulSoup(response.text, "html.parser")
        if response.status_code != self.returncode:
            response.failure(requestFailureMessage(self, response))
        else:
            json_object = json.loads(soup.string)
            courseId = str(json_object["createdCourse"]["id"])
            self.createdCourses.append(courseId)
            return (courseId)

def deleteCourse(self, courseId):
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
        if response.status_code != self.returncode:
            response.failure(requestFailureMessage(self, response))

def lernStore(self):  
    '''
    Creates a Course which 
    '''

    # Create Course
    courseId = createCourse(self, courseDataBuilder(self))    

    # Add Resources
    if isinstance(self._user, locustfile.TeacherUser):
        thema_data = themaDataBuilder(self, courseId, "resources")

        # Adding a theme to the course to be able to add material from the Lernstore
        with self.client.request("POST",
            "/courses/" + courseId + "/topics",
            name="/courses/topics",
            data=thema_data,
            catch_response=True,
            allow_redirects=True
        ) as response:
            if response.status_code != self.returncode:
                response.failure(requestFailureMessage(self, response))

            # Request to the Lernstore to get the internal id of the course
            with self.client.request("GET",
                "https://api.staging.niedersachsen.hpi-schul-cloud.org/lessons?courseId=" + courseId,
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
                    "https://api.staging.niedersachsen.hpi-schul-cloud.org/lessons/" + courseId_Lernstore + "/material",
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
                    if response.status_code != 201:
                        response.failure(requestFailureMessage(self, response))
    # Delete Course
    deleteCourse(self, courseId)

def courseAddEtherPadAndTool(self):

    # Create Course
    courseId = createCourse(self, courseDataBuilder(self))

    # Add Etherpads
    if isinstance(self._user, locustfile.TeacherUser):
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
            if response.status_code != self.returncode:
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
            data = "privacy_permission=anonymous&openNewTab=true&name=bettermarks&url=https://acc.bettermarks.com/Fv1.0/schulcloud/de_ni_staging/login&key=&logo_url=https://acc.bettermarks.com/app/assets/bm-logo.png&isLocal=true&resource_link_id=&lti_version=&lti_message_type=&isTemplate=false&skipConsent=false&createdAt=2021-01-14T13:35:44.689Z&updatedAt=2021-01-14T13:35:44.689Z&__v=0&originTool=600048b0755565002840fde4&courseId=" + str(courseId),
            catch_response=True,
            allow_redirects=True
        ) as response:
            with self.client.request("GET",
                "https://acc.bettermarks.com/v1.0/schulcloud/de_ni_staging/login",
                catch_response=True,
                allow_redirects=True
            ) as response:
                if response.status_code != self.returncode:
                    response.failure(requestFailureMessage(self, response))

    # Delete Course
    deleteCourse(self, courseId)

def createDeleteTeam(self):
    '''
    Can be called as a task for the loadtest. Creates a new team and deletes it afterwards.
    '''
    
    teamId = newTeam(self)
    deleteTeam(self, teamId)

def newTeam(self):
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
        if response.status_code != self.returncode:
            response.failure(requestFailureMessage(self, response))
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            teamIdString = soup.find_all("section", {"class": "section-teams"})
            teamId = str(teamIdString).partition('\n')[0][41:65]
            self.createdTeams.append(teamId)
            
    return teamId

def deleteTeam(self, teamID):
    header = requestHeaderBuilder(self, (self.user.host + "/teams/" + teamID + "/edit"))
    header["accept"] = "*/*"
    header["accept-language"] = "en-US,en;q=0.9"
    
    with self.client.request("DELETE",
        "/teams/" + teamID + "/" ,
        headers = header,
        name="/teams/delete",
        catch_response=True,
        allow_redirects=True
    ) as response:
        if response.status_code != self.returncode:
            response.failure(requestFailureMessage(self, response))
            return False
        else:
            return True

def matrixMessenger(self):
    txn_id = 0
    mainHost = os.environ.get("MMHOST")
    with self.client.request("GET", "/messenger/token", catch_response=True, allow_redirects=False) as response:
                if(response.status_code == 200):
                    i = json.loads(response.text)
                    self.token = i["accessToken"]
                    self.user_id = i["userId"]

    room_ids = None
    with self.client.get("/courses/" , catch_response=True, allow_redirects=True) as response:
        if(response.status_code == 200):
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
                    mainHost + "/r0/rooms/" + room_id + "/send/m.room.message",
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

    self.client.get(mainHost + "/versions")

    self.client.get(mainHost + "/r0/voip/turnServer")

    self.client.get(mainHost + "/r0/pushrules/")

    self.client.get(mainHost + "/r0/joined_groups")

    self.client.get(mainHost + "/r0/profile/" + self.user_id)