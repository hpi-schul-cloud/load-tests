import logging
import sys
import yaml
import os
import random

from loadtests import constant
from urllib.parse import urlparse
from locust import HttpUser
from loadtests.bbbTaskSet import bbbTaskSet
from loadtests.scTaskSet import scTaskSet
from loadtests.docTaskSet import docTaskSet
from loadtests.reqWithoutUserTaskSet import reqWithoutUserTaskSet
from loadtests.rocketChatTaskSet import rocketChatTaskSet

class PupilUser(HttpUser):
    '''
    Representing a pupil user on the SchulCloud.
    '''

    weight = 5 # specifys how often the loadtest should simulate this user-type.
    tasks = {bbbTaskSet:1, scTaskSet:3, docTaskSet:1, reqWithoutUserTaskSet:1, rocketChatTaskSet:1} # collection of taks-sets which can be applied to the user
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
    tasks = {bbbTaskSet:1, scTaskSet:3, docTaskSet:1, reqWithoutUserTaskSet:1, rocketChatTaskSet:1} # collection of taks-sets which can be applied to the user
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
    tasks = {bbbTaskSet:1, scTaskSet:3, docTaskSet:1, reqWithoutUserTaskSet:1, rocketChatTaskSet:1} # collection of taks-sets which can be applied to the user
    wait_time = constant.constant.wait_time # specifys the waiting time after finishing a task and starting the next
    user_type = "teacher" # specifys the type of the user
    login_credentials = None # gives the user log-in credentials for further actions

    def __init__(self, *args, **kwargs):
        super(TeacherUser, self).__init__(*args, **kwargs)
        getUserCredentials(self)


def getUserCredentials(user):
    '''
    Configuers the login credentials for the provided user. If the user credentials are stored at a (lokal) .yaml
    file, these credentials will be used. Other wise environment-variables will be used as login-credentials.

    Param:
        user (HttpUser) : user which calls for new credentials
    '''

    logger = logging.getLogger(__name__)

    try:
        filename = constant.constant.userCredentialsFilePath
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                yaml_loaded = yaml.safe_load(file)
                if (yaml_loaded != None) and (user.user_type in yaml_loaded):
                    user.login_credentials = random.choice(yaml_loaded[user.user_type])
        else:
            logger.error("File does not exist: " + filename)
            sys.exit(1)
    except:
        if user.user_type == 'admin' and constant.constant.loginCredentialsAdmin['email'] is not None and constant.constant.loginCredentialsAdmin['password'] is not None:
            user.login_credentials = constant.constant.loginCredentialsAdmin
        elif user.user_type == 'teacher' and constant.constant.loginCredentialsTeacher['email'] is not None and constant.constant.loginCredentialsTeacher['password'] is not None:
            user.login_credentials = constant.constant.loginCredentialsTeacher
        elif user.user_type == 'pupil' and constant.constant.loginCredentialsPupil['email'] is not None and constant.constant.loginCredentialsPupil['password'] is not None:
            user.login_credentials = constant.constant.loginCredentialsPupil
        else:
            logger.error("User not found: " + user.user_type)
            sys.exit(1)

    if user.login_credentials == None:
        logger.info("No %s users found in " + filename, user.user_type)
