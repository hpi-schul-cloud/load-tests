import logging
import random

from locust import HttpUser


from loadtests.shared import constant
from loadtests.loadtests.bbbTaskSet import bbbTaskSet
from loadtests.loadtests.scTaskSet import scTaskSet
from loadtests.loadtests.docTaskSet import docTaskSet
from loadtests.loadtests.reqWithoutUserTaskSet import reqWithoutUserTaskSet
from loadtests.loadtests.rocketChatTaskSet import rocketChatTaskSet
from loadtests.loadtests.statusServiceTaskSet import statusServiceTaskSet

class PupilUser(HttpUser):
    '''
    Representing a pupil user on the SchulCloud.
    '''

    weight = constant.Constant.pupilWeight # specifys how often the loadtest should simulate this user-type.
    tasks = {bbbTaskSet:1, scTaskSet:3, docTaskSet:1, reqWithoutUserTaskSet:1, rocketChatTaskSet:1} # collection of taks-sets which can be applied to the user
    user_type = "pupil" # specifys the type of the user
    login_credentials = constant.Constant.loginCredentialsPupil # gives the user log-in credentials for further actions
    wait_time = random.randint(constant.Constant.timeToWaitShort, constant.Constant.timeToWaitLong)

    def __init__(self, *args, **kwargs):
        super(PupilUser, self).__init__(*args, **kwargs)

class AdminUser(HttpUser):
    '''
    Representing a admin user on the SchulCloud.
    '''

    weight = constant.Constant.adminWeight # specifys how often the loadtest should simulate this user-type
    tasks = {bbbTaskSet:1, scTaskSet:3, docTaskSet:1, reqWithoutUserTaskSet:1, rocketChatTaskSet:1} # collection of taks-sets which can be applied to the user
    user_type = "admin" # specifys the type of the user
    login_credentials = constant.Constant.loginCredentialsAdmin # gives the user log-in credentials for further actions
    wait_time = random.randint(constant.Constant.timeToWaitShort, constant.Constant.timeToWaitLong)

    def __init__(self, *args, **kwargs):
        super(AdminUser, self).__init__(*args, **kwargs)

class TeacherUser(HttpUser):
    '''
    Representing a teacher user on the SchulCloud.
    '''

    weight = constant.Constant.teacherWeight # specifys how often the loadtest should simulate this user-type.
    tasks = {bbbTaskSet:1, scTaskSet:3, docTaskSet:1, reqWithoutUserTaskSet:1, rocketChatTaskSet:1} # collection of taks-sets which can be applied to the user
    user_type = "teacher" # specifys the type of the user
    login_credentials = constant.Constant.loginCredentialsTeacher # gives the user log-in credentials for further actions
    wait_time = random.randint(constant.Constant.timeToWaitShort, constant.Constant.timeToWaitLong)

    def __init__(self, *args, **kwargs):
        super(TeacherUser, self).__init__(*args, **kwargs)

class AnonymousUser(HttpUser):
    '''
    Representing a teacher user on the SchulCloud.
    '''

    weight = constant.Constant.anonymousWeight # specifys how often the loadtest should simulate this user-type.
    tasks = {bbbTaskSet:0, scTaskSet:0, docTaskSet:0, reqWithoutUserTaskSet:1, statusServiceTaskSet:1, rocketChatTaskSet:0} # collection of taks-sets which can be applied to the user
    user_type = "anonymous" # specifys the type of the user
    login_credentials = None # gives the user log-in credentials for further actions
    wait_time = random.randint(constant.Constant.timeToWaitShort, constant.Constant.timeToWaitLong)

    def __init__(self, *args, **kwargs):
        super(AnonymousUser, self).__init__(*args, **kwargs)


