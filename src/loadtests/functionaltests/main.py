import sys
import time
import logging
import threading
from typing import Optional

from gevent import monkey
# monkey-patch the monkey patch because it prevents debugging and has no use here
monkey.patch_all = lambda *args, **kwargs: ()

from prometheus_client import start_http_server, Gauge

from loadtests.functionaltests.functionalTester import FunctionalTester


TIMEINTERVAL_SEC = 300
PROMETHEUS_PORT = 9000
HOSTS = [
    ('staging_niedersachsen', 'https://staging.niedersachsen.dbildungscloud.org')
]


global_logger = logging.getLogger(__name__)


class Host:
    # constructor header must fit HOSTS
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.temp_failure_counter = 0
        self.temp_exception_counter = 0
        self.failure_counter = Gauge(f'functional_failure_{name}', f'How many functional tests failed in {name}')
        self.exception_counter = Gauge(f'functional_exception_{name}', f'How many exceptions happened in functional tests in {name}')


class TestThread:
    def __init__(self, host: Host):
        self.host = host
        self.thread: Optional[threading.Thread] = None
        self.logger = logging.getLogger(host.name)

    def run(self):
        self.logger.info(f'Starting thread for {self.host.name}')
        self.thread = threading.Thread(target=self._run_functional_tester)
        self.thread.start()

    def join(self):
        if self.thread:
            self.thread.join()
            self.thread = None
            self.logger.info(f'Thread has ended for {self.host.name}')
        else:
            self.logger.warning(f'Cannot join non-existing thread')

    def _run_functional_tester(self):
        def failure_callback(task_name, info):
            self.logger.warning(f'test failure: {task_name}, {info}')
            self.host.temp_failure_counter += 1

        def exception_callback(task_name, exc):
            self.logger.warning(f'test exception: {task_name}, {type(exc).__name__}: {exc}')
            self.host.temp_exception_counter += 1

        tester = FunctionalTester(self.host.url, failure_callback, exception_callback, self.logger)
        self.host.temp_failure_counter = 0
        self.host.temp_exception_counter = 0
        tester.run()
        self.host.failure_counter.set(self.host.temp_failure_counter)
        self.host.exception_counter.set(self.host.temp_exception_counter)


def main():
    logging.basicConfig(level=logging.INFO)  # override locust logging config
    start_http_server(PROMETHEUS_PORT)
    threads = [TestThread(Host(*host)) for host in HOSTS]
    while True:
        global_logger.info('Starting functional tests...')
        start_time = time.time()
        for thread in threads:
            thread.run()
        for thread in threads:
            thread.join()
        remaining_sleep = TIMEINTERVAL_SEC - (time.time() - start_time)
        if remaining_sleep > 0:
            global_logger.info(f'Sleeping for {remaining_sleep} seconds...')
            time.sleep(remaining_sleep)


if __name__ == '__main__':
    main()
