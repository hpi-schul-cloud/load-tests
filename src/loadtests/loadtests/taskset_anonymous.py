from locust.user.task import TaskSet, tag, task

from loadtests.loadtests.constant import StatusCode


class TasksetAnonymous(TaskSet):
    """
        Taskset to make sure certain things work without logging in
    """

    @tag('anonymous_version')
    @task
    def anonymous_version(self):
        """
        Request of API, domain and nuxtversion of a supplied domain without a user.
        """

        response = self.client.get(f"{self.user.host}/version", catch_response=True)
        if response.status_code != StatusCode.OK:
            response.failure(f"req failed : {response.status_code} - {response.headers}")

        nuxt_response = self.client.get(f"{self.user.host}/nuxtversion", catch_response=True)
        if nuxt_response.status_code != StatusCode.OK:
            nuxt_response.failure(f"nuxt_req failed : {nuxt_response} - {nuxt_response.headers}")
