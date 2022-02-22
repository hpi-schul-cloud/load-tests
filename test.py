
import locust
from locust.env import Environment
from loadtests.loadtests.locustfile import *


def main():
    host = 'https://agmonlog-1.hpi-schul-cloud.dev'
    
    # locust set up code
    for user_class in user_classes:
        user_class.host = host

    env = Environment()
    env.events = locust.Events()
    env.events.request_success.add_listener(lambda **kw: print('request_success:', kw))
    env.events.request_failure.add_listener(lambda **kw: print('request_failure:', kw))
    env.events.test_start.add_listener(lambda **kw: print('test_start:', kw))
    env.events.test_stop.add_listener(lambda **kw: print('test_stop:', kw))
    
    #run all tasks
    for user_class in user_classes:
        user = user_class(env)
        user.on_start()
        for taskset_class in user.tasks.keys():
            taskset = taskset_class(user)
            taskset.on_start()
            # TODO: run every task of taskset
            taskset.on_stop()
        user.on_stop()

    
    # example of a single task
    admin = AdminUser(env)
    taskset = scTaskSet(admin)
    
    admin.on_start()
    taskset.on_start()
    taskset.index()
    taskset.on_stop()
    admin.on_stop()


if __name__ == '__main__':
    main()