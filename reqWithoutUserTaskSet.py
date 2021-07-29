import constant

from locust.user.task import TaskSet, tag, task

class reqWithoutUserTaskSet(TaskSet):

    @tag('reqWithoutUser')
    @task
    def requestWithoutUser(self):
        '''
        Request of API, domain and nuxtversion of a supplied domain without a user.

        Args:
            url (str) : domain to which the requests should be send (importet from constant)
        '''
        url = constant.constant.urlReqWithoutUser
        with self.client.get("https://api." + url + "/version", name="/api/version") as api_response:
            if api_response.status_code != constant.constant.returncodeNormal:
                api_response.failure(f"API response failed : {api_response} - {api_response.headers}")

        with self.client.get("https://" + url + "/version") as response:
            if response.status_code != constant.constant.returncodeNormal:
                response.failure(f"req failed : {response.status_code} - {response.headers}")

        with self.client.get("https://" + url + "/nuxtversion") as nuxt_response:
            if nuxt_response.status_code != constant.constant.returncodeNormal:
                nuxt_response.failure(f"nuxt_req failed : {nuxt_response} - {nuxt_response.headers}")