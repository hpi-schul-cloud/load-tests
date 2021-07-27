import logging
import sys
import yaml
import os
import random
import constant

from urllib.parse import urlparse
from locust import HttpUser, between
class PupilUser(HttpUser):
    ''' 
    Representing a pupil user on the SchulCloud.
    
    Args:
        weight (int) : specifys how often the loadtest should simulate this user-type.
        tasks (dictionary) : collection of taks-sets which can be applied to the user
        wait_time (int) : specifys the waiting time after finishing a task and starting the next
        user_type (str) : specifys the type of the user
        login_credentials (str) : gives the user log-in credentials for further actions
    '''

    weight = 5
    tasks = constant.constant.tasks
    wait_time = constant.constant.wait_time
    user_type = "pupil"
    login_credentials = None

    def __init__(self, *args, **kwargs):
        super(PupilUser, self).__init__(*args, **kwargs)
        getUserCredentials(self)

class AdminUser(HttpUser):
    ''' 
    Representing a admin user on the SchulCloud.
    
    Args:
        weight (int) : specifys how often the loadtest should simulate this user-type.
        tasks (dictionary) : collection of taks-sets which can be applied to the user
        wait_time (int) : specifys the waiting time after finishing a task and starting the next
        user_type (str) : specifys the type of the user
        login_credentials (str) : gives the user log-in credentials for further actions
    '''

    weight = 1
    tasks = constant.constant.tasks
    wait_time = constant.constant.wait_time
    user_type = "admin"
    login_credentials = None

    def __init__(self, *args, **kwargs):
        super(AdminUser, self).__init__(*args, **kwargs)
        getUserCredentials(self)

class TeacherUser(HttpUser):
    ''' 
    Representing a teacher user on the SchulCloud.
    
    Args
        weight (int) : specifys how often the loadtest should simulate this user-type.
        tasks (dictionary) : collection of taks-sets which can be applied to the user
        wait_time (int) : specifys the waiting time after finishing a task and starting the next
        user_type (str) : specifys the type of the user
        login_credentials (str) : gives the user log-in credentials for further actions
    '''
    
    weight = 3
    tasks = constant.constant.tasks
    wait_time = constant.constant.wait_time
    user_type = "teacher"
    login_credentials = None

    def __init__(self, *args, **kwargs):
        super(TeacherUser, self).__init__(*args, **kwargs)
        getUserCredentials(self)


def getUserCredentials(user):
    '''
    Configuers the login credentials for the provided user.

    Param:
        user (HttpUser) : user which calls for new credentials

    Args:
        logger
        hostname (str) : name of the host
        filename (str) : url to file which contains login credentials
    '''

    logger = logging.getLogger(__name__)

    hostname = urlparse(user.host).hostname
    filename = "./users_" + hostname + ".yaml"
    if not os.path.exists(filename):
        logger.error("File does not exist: " + filename)
        sys.exit(1)

    with open(filename, 'r') as file:
        yaml_loaded = yaml.safe_load(file)
        if (yaml_loaded != None) and (user.user_type in yaml_loaded):
            user.login_credentials = random.choice(yaml_loaded[user.user_type])

    if user.login_credentials == None:
        logger.info("No %s users found in " + filename, user.user_type)
