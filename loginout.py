import base64
import json

from bs4 import BeautifulSoup


def login(self):
    # First task. Gets csrf token from login html website and logs in.
    # Gets bearer token after login from the response header and extracts specific informations for further progress.
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
                response_header = login_post_response.headers
                self.bearer_token = (response_header["set-cookie"]).split(";")[0].replace("jwt=", "")
                decoded_token = base64.b64decode(self.bearer_token[0:461])
                decoded_token_json = json.loads(decoded_token.decode('utf_8').removeprefix('{"alg":"HS256","typ":"access"}'))
                self.user_id = decoded_token_json["userId"]
                self.school_id = decoded_token_json["schoolId"]
                self.account_id = decoded_token_json["accountId"]
                self.roles_id = decoded_token_json["roles"]
                self.iat = decoded_token_json["iat"]
                self.jti = decoded_token_json["jti"]
    return self

def logout(self):
    self.client.get("/logout/", allow_redirects=True)
    self.csrf_token = None