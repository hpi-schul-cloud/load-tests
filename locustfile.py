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
    '''

    weight = 5 # specifys how often the loadtest should simulate this user-type.
    tasks = constant.constant.tasks # collection of taks-sets which can be applied to the user
    wait_time = constant.constant.wait_time # specifys the waiting time after finishing a task and starting the next
    user_type = "pupil" # specifys the type of the user
    login_credentials = None # gives the user log-in credentials for further actions

    def __init__(self, *args, **kwargs):
        super(PupilUser, self).__init__(*args, **kwargs)
        getUserCredentials(self)

class AdminUser(HttpUser):
    ''' 
    Representing a admin user on the SchulCloud.
    '''

    weight = 1 # specifys how often the loadtest should simulate this user-type
    tasks = constant.constant.tasks # collection of taks-sets which can be applied to the user
    wait_time = constant.constant.wait_time # specifys the waiting time after finishing a task and starting the next
    user_type = "admin" # specifys the type of the user
    login_credentials = None # gives the user log-in credentials for further actions

    def __init__(self, *args, **kwargs):
        super(AdminUser, self).__init__(*args, **kwargs)
        getUserCredentials(self)

class TeacherUser(HttpUser):
    ''' 
    Representing a teacher user on the SchulCloud.
    '''
    
    weight = 3 # specifys how often the loadtest should simulate this user-type.
    tasks = constant.constant.tasks # collection of taks-sets which can be applied to the user
    wait_time = constant.constant.wait_time # specifys the waiting time after finishing a task and starting the next
    user_type = "teacher" # specifys the type of the user
    login_credentials = None # gives the user log-in credentials for further actions

    def __init__(self, *args, **kwargs):
        super(TeacherUser, self).__init__(*args, **kwargs)
        getUserCredentials(self)


def getUserCredentials(user):
    '''
    Configuers the login credentials for the provided user.

    Param:
        user (HttpUser) : user which calls for new credentials
    '''

    logger = logging.getLogger(__name__)

    hostname = urlparse(user.host).hostname # name of the host
    filename = "./users_" + hostname + ".yaml" # url to file which contains login credentials
    if not os.path.exists(filename):
        logger.error("File does not exist: " + filename)
        sys.exit(1)

    with open(filename, 'r') as file:
        yaml_loaded = yaml.safe_load(file)
        if (yaml_loaded != None) and (user.user_type in yaml_loaded):
            user.login_credentials = random.choice(yaml_loaded[user.user_type])

    if user.login_credentials == None:
        logger.info("No %s users found in " + filename, user.user_type)
