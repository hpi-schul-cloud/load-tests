from loadtests import constant

from locust.user.task import TaskSet, tag, task

from loadtests.requestsBuilder import normalGET, requestFailureMessage

class statusServiceTaskSet(TaskSet):

    @tag('statusService')
    @task
    def simpleRequest(self):
        '''
        Request of API, domain and nuxtversion of a supplied domain without a user.

        Param:
            self (TaskSet): TaskSet
        '''
        url = f"{self.user.host}"
        with self.client.get(url, catch_response=True, allow_redirects=True) as response:
            if response.status_code != constant.constant.returncodeNormal:
                response.failure(requestFailureMessage(self, response))

    @tag('statusService')
    @tag('statusServiceApi')
    @task
    def componentsApiRequest(self):
        '''
        Request of API, domain and nuxtversion of a supplied domain without a user.

        Param:
            self (TaskSet): TaskSet
        '''
        url = f"{self.user.host}"
        with self.client.get(url+"/api/v1/components", catch_response=True, allow_redirects=True) as response:
            if response.status_code != constant.constant.returncodeNormal:
                response.failure(requestFailureMessage(self, response))

    @tag('statusService')
    @tag('statusServiceApi')
    @task
    def incidentsApiRequest(self):
        '''
        Request of API, domain and nuxtversion of a supplied domain without a user.

        Param:
            self (TaskSet): TaskSet
        '''
        url = f"{self.user.host}"
        with self.client.get(url+"/api/v1/incidents", catch_response=True, allow_redirects=True) as response:
            if response.status_code != constant.constant.returncodeNormal:
                response.failure(requestFailureMessage(self, response))
