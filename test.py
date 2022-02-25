
from pyclbr import Function
import locust
from locust.env import Environment
import loadtests.loadtests.locustfile as locustfile


class FunctionalTester:

    def __init__(self, host: str):
        self.host = host
    
        # locust set up code
        for user_class in locustfile.user_classes:
            user_class.host = self.host

        self.env = Environment()
        self.env.events = locust.Events()
        self.env.events.request_success.add_listener(lambda **kw: print('request_success:', kw))
        self.env.events.request_failure.add_listener(lambda **kw: print('request_failure:', kw))
        self.env.events.test_start.add_listener(lambda **kw: print('test_start:', kw))
        self.env.events.test_stop.add_listener(lambda **kw: print('test_stop:', kw))
    
    def run(self):
        #self.run_all()
        self.example_of_running_single_task()

    def example_of_running_single_task(self): 
        admin = locustfile.AdminUser(self.env)
        taskset = locustfile.scTaskSet(admin)

        admin.on_start()
        taskset.on_start()

        taskset.index()
        
        taskset.on_stop()
        admin.on_stop()
    
    def run_all(self):
        for user_class in locustfile.user_classes:
            user = user_class(self.env)
            user.on_start()
            for taskset_class in user.tasks:
                taskset = taskset_class(user)
                taskset.on_start()  # TODO: login/logout in user.on_start() ?
                # TODO: get all task from taskset and run them one by one
                # e.g.: for task in taskset.task:
                #           task()
                taskset.on_stop()
            user.on_stop()


if __name__ == '__main__':
    tester = FunctionalTester('https://agmonlog-1.hpi-schul-cloud.dev')
    tester.run()
