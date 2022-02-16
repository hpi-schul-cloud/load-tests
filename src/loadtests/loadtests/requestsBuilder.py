from bs4 import BeautifulSoup

from loadtests.shared import constant

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
                if response.status_code != Constant.returncodeNormal:
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
        if response.status_code != Constant.returncodeNormal:
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
        "untilDate"             : "31.07.2023",
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

    Param:
        self: Taskset
        courseId: Course ID
        components:
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
