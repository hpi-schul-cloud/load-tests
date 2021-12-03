from loadtests import constant

from locust.user.task import TaskSet, tag, task

from loadtests.requestsBuilder import normalGET

class statusServiceTaskSet(TaskSet):

    @tag('statusService')
    @task
    def simpleRequest(self):
        '''
        Request of API, domain and nuxtversion of a supplied domain without a user.

        Param:
            self (TaskSet): TaskSet
        '''
        normalGET(self, "/")
