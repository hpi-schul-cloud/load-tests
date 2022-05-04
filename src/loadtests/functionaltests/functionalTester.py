
import logging
import sys
from typing import Optional

from locust.env import Environment, Events
from loadtests.loadtests import locustfile


class FunctionalTester:

    def __init__(self, host: str, failure_callback, exception_callback, logger: logging.Logger):
        self.host = host
        self.task_name = None
        self.failure_callback = failure_callback
        self.exception_callback = exception_callback

        # locust set up code
        for user_class in locustfile.user_classes:
            user_class.host = self.host

        self.logger = logger

        self.env = Environment()
        self.env.events = Events()
        self.env.events.request_failure.add_listener(lambda **kw: self.failure_callback(self.task_name, kw))
        self.env.events.test_start.add_listener(lambda **kw: self.logger.info('test_start:', kw))
        self.env.events.test_stop.add_listener(lambda **kw: self.logger.info('test_stop:', kw))

    def run(self):
        self.run_all()

    def run_all(self):
        for user_class in locustfile.user_classes:
            user = user_class(self.env)
            self.logger.info(f'User: {type(user).__name__}')

            self.task_name = 'user.on_start'
            user.on_start()

            for taskset_class in user.tasks:
                taskset = taskset_class(user)
                self.logger.info(f'  TaskSet: {type(taskset).__name__}')

                self.task_name = 'taskset.on_start'
                try:
                    taskset.on_start()
                except Exception as exc:
                    self.exception_callback(self.task_name, exc)

                for task in taskset.tasks:
                    self.task_name = task.__name__
                    self.logger.info(f'    {self.task_name}')
                    try:
                        task(taskset)
                    except Exception as exc:
                        self.exception_callback(self.task_name, exc)

                self.task_name = 'taskset.on_stop'
                try:
                    taskset.on_stop()
                except Exception as exc:
                    self.exception_callback(self.task_name, exc)

            self.task_name = 'user.on_stop'
            user.on_stop()
