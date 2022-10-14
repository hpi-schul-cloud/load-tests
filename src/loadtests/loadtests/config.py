import os
import logging
from urllib.parse import urlparse, urljoin
from typing import Any

missing_env_vars = False
logger = logging.getLogger(__name__)

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

def normalize_url(domain: str):
    url: str = ""
    u = urlparse(domain)
    mynetloc = u.netloc
    mypath = u.path
    myscheme = "https://"

    if mynetloc != "":
        url = myscheme + mynetloc
    else:
        if mypath != "":
                url = myscheme + mypath
        else:
            logger.error(f'Specified domain variable {domain} not correct')
    return url

class Config:
    FUNCTIONAL_TEST = bool(get_environment_var("FUNCTIONAL_TEST", int, default=0))
    LOADTEST_EXTERNAL = bool(get_environment_var("LOADTEST_EXTERNAL", int, default=1))
    DEBUG_LEVEL = int(get_environment_var("DEBUG_LEVEL", int, default=20)) # 10 == Debug, 20 = Info, 30 == Warn, 40 == Error
    if FUNCTIONAL_TEST:
        print("Do Functional Test")
        BBB_ROOM_COUNT = 1
        BBB_USER_COUNT = 2
        WEIGHT_ADMIN = 1
        WEIGHT_TEACHER = 1
        WEIGHT_PUPIL = 1
        WEIGHT_ANONYMOUS = 1
        WEIGHT_ACTUAL_ANONYMOUS = 1
        WAIT_TIME_SHORT = 1
        WAIT_TIME_LONG = 10
        TIMEINTERVAL_SEC = get_environment_var('TIMEINTERVAL_SEC', int, default=300)
        PROMETHEUS_PORT = get_environment_var('PROMETHEUS_PORT', int, default=9000)
        TARGET_URL = normalize_url(get_environment_var('TARGET_URL'))
    elif LOADTEST_EXTERNAL:
        print("Do Load Test External setting")
        BBB_ROOM_COUNT = 0
        BBB_USER_COUNT = 0
        WEIGHT_ADMIN = 0
        WEIGHT_TEACHER = 0
        WEIGHT_PUPIL = 0
        WEIGHT_ANONYMOUS = 0
        WEIGHT_ACTUAL_ANONYMOUS = 0
        WEIGHT_EXTERNAL_PUPIL = 1
        WAIT_TIME_SHORT = 1
        WAIT_TIME_LONG = 1
    else:  # load test
        print("Do Load Test (Default setting)")
        BBB_ROOM_COUNT = get_environment_var("BBBNUMBERROOMS", int, 0)
        BBB_USER_COUNT = get_environment_var("BBBNUMBERUSERS", int, 0)
        WEIGHT_ADMIN = get_environment_var("ADMIN_WEIGHT", int, 1)
        WEIGHT_TEACHER = get_environment_var("TEACHER_WEIGHT", int, 1)
        WEIGHT_PUPIL = get_environment_var("PUPIL_WEIGHT", int, 1)
        WEIGHT_ANONYMOUS = get_environment_var("ANONYMOUS_WEIGHT", int, 0)
        WEIGHT_ACTUAL_ANONYMOUS = get_environment_var("ACTUAL_ANONYMOUS_WEIGHT", int, default=1)
        WAIT_TIME_SHORT = get_environment_var("TIMESHORT", int, 1)
        WAIT_TIME_LONG = get_environment_var("TIMELONG", int, 1)

    # URL and Port for the chromedriver Pod
    BROWSER_IP_PORT = get_environment_var("BROWSERIPPORT", default="localhost:4444")

    # required for downloading bettermarks-tools
    #urlBetterMarks = getEnvironmentVariable("URLBETTERMARKS")

    LOGIN_ADMIN = {
        'email': get_environment_var("ADMIN_EMAIL", default="admin@schul-cloud.org"),
        'password': get_environment_var("ADMIN_PASSWORD", default="Schulcloud1!")
    }
    LOGIN_TEACHER = {
        'email': get_environment_var("TEACHER_EMAIL", default="lehrer@schul-cloud.org"),
        'password': get_environment_var("TEACHER_PASSWORD", default="Schulcloud1!")
    }
    LOGIN_PUPIL = {
        'email': get_environment_var("PUPIL_EMAIL", default="schueler@schul-cloud.org"),
        'password': get_environment_var("PUPIL_PASSWORD", default="Schulcloud1!")
    }
    LOGIN_ANONYMOUS = {
        'email': get_environment_var("ANONYMOUS_EMAIL", default="schueler@schul-cloud.org"),
        'password': get_environment_var("ANONYMOUS_PASSWORD", default="Schulcloud1!")
    }
    LOGIN_EXTERN_PUPIL = {
        'email': get_environment_var("EXTERN_PUPIL_EMAIL", default="emil.extern"),
        'password': get_environment_var("EXTERN_PUPIL_PASSWORD", default="Extern1!")
    }

    if missing_env_vars:
        raise RuntimeError('Missing environment variables. Check error log.')
