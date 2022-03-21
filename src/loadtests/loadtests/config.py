
import logging
import os
from typing import Any


logger = logging.getLogger(__name__)
missing_env_vars = False


def get_environment_var(name: str, dtype: type = None, default: Any = None):
    global missing_env_vars
    var = os.getenv(name)
    if var:
        if dtype:
            var = dtype(var)
        return var
    else:
        if default is None:
            logger.error(f'Environment variable {name} not found but required')
            missing_env_vars = True
        return default


class Config:
    FUNCTIONAL_TEST = bool(get_environment_var("FUNCTIONAL_TEST", int, default=0))
    if FUNCTIONAL_TEST:
        BBB_ROOM_COUNT = 1
        BBB_USER_COUNT = 2
        WEIGHT_ADMIN = 1
        WEIGHT_TEACHER = 1
        WEIGHT_PUPIL = 1
        WEIGHT_ANONYMOUS = 1
        WEIGHT_ACTUAL_ANONYMOUS = 1
        WAIT_TIME_SHORT = 1
        WAIT_TIME_LONG = 1
    else:  # load test
        BBB_ROOM_COUNT = get_environment_var("BBBNUMBERROOMS", int)
        BBB_USER_COUNT = get_environment_var("BBBNUMBERUSERS", int)
        WEIGHT_ADMIN = get_environment_var("ADMIN_WEIGHT", int)
        WEIGHT_TEACHER = get_environment_var("TEACHER_WEIGHT", int)
        WEIGHT_PUPIL = get_environment_var("PUPIL_WEIGHT", int)
        WEIGHT_ANONYMOUS = get_environment_var("ANONYMOUS_WEIGHT", int)
        WEIGHT_ACTUAL_ANONYMOUS = get_environment_var("ACTUAL_ANONYMOUS_WEIGHT", int, default=1)
        WAIT_TIME_SHORT = get_environment_var("TIMESHORT", int)
        WAIT_TIME_LONG = get_environment_var("TIMELONG", int)

    # URL and Port for the chromedriver Pod
    BROWSER_IP_PORT = get_environment_var("BROWSERIPPORT", default="chromedriver-svc:4444")

    # required for downloading bettermarks-tools
    #urlBetterMarks = getEnvironmentVariable("URLBETTERMARKS")

    LOGIN_ADMIN = {
        'email': get_environment_var("ADMIN_EMAIL"),
        'password': get_environment_var("ADMIN_PASSWORD")
    }
    LOGIN_TEACHER = {
        'email': get_environment_var("TEACHER_EMAIL"),
        'password': get_environment_var("TEACHER_PASSWORD")
    }
    LOGIN_PUPIL = {
        'email': get_environment_var("PUPIL_EMAIL"),
        'password': get_environment_var("PUPIL_PASSWORD")
    }
    LOGIN_ANONYMOUS = {
        'email': get_environment_var("ANONYMOUS_EMAIL"),
        'password': get_environment_var("ANONYMOUS_PASSWORD")
    }

    if missing_env_vars:
        raise RuntimeError('Missing environment variables. Check error log.')
