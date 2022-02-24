
import locust
from locust.env import Environment
import loadtests.loadtests.locustfile as locustfile


class FunctionalTester:

    def __init__(self, host: str):
        self.host = host
        self.task_name = None
    
        # locust set up code
        for user_class in locustfile.user_classes:
            user_class.host = self.host

        self.env = Environment()
        self.env.events = locust.Events()
        #self.env.events.request_success.add_listener(lambda **kw: print('request_success:', kw))
        self.env.events.request_failure.add_listener(lambda **kw: print('request_failure:', self.task_name))  #, kw))
        self.env.events.test_start.add_listener(lambda **kw: print('test_start:', kw))
        self.env.events.test_stop.add_listener(lambda **kw: print('test_stop:', kw))
    
    def run(self):
        self.run_all()

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
            print('\nUser:', user.user_type)
            self.task_name = 'user.on_start'
            user.on_start()
            for taskset_class in [locustfile.scTaskSet]:
                taskset = taskset_class(user)
                print('\nTaskSet:', type(taskset).__name__)
                self.task_name = 'taskset.on_start'
                taskset.on_start()
                for task in taskset.tasks:
                    self.task_name = task.__name__
                    #if not self.task_name == 'createDeleteTeam':
                    #    continue
                    print(self.task_name)
                    task(taskset)
                self.task_name = 'taskset.on_stop'
                taskset.on_stop()
            self.task_name = 'user.on_stop'
            user.on_stop()

