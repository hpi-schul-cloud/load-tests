
from locust.user.task import tag, task

from loadtests.loadtests.constant import StatusCode
from loadtests.loadtests.taskset_base import TasksetBase


class TasksetStatusService(TasksetBase):

    @tag('statusService')
    @task
    def simple_request(self):
        url = f"{self.user.host}"
        with self.client.get(url, catch_response=True, allow_redirects=True) as response:
            if response.status_code != StatusCode.OK:
                response.failure(self.request_failure_message(response))

    @tag('statusService')
    @tag('statusServiceApi')
    @task
    def components_api_request(self):
        url = f"{self.user.host}"
        with self.client.get(f"{url}/api/v1/components", catch_response=True, allow_redirects=True) as response:
            if response.status_code != StatusCode.OK:
                response.failure(self.request_failure_message(response))

    @tag('statusService')
    @tag('statusServiceApi')
    @task
    def incidents_api_request(self):
        url = f"{self.user.host}"
        with self.client.get(f"{url}/api/v1/incidents", catch_response=True, allow_redirects=True) as response:
            if response.status_code != StatusCode.OK:
                response.failure(self.request_failure_message(response))
