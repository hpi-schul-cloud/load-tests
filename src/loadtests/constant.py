import os

from loadtests.bbbTaskSet import *
from loadtests.scTaskSet import *
from loadtests.docTaskSet import *
from loadtests.reqWithoutUserTaskSet import *
from loadtests.rocketChatTaskSet import *
from locust import between

class constant():
    wait_time = between(5, 15) # Provides a random number which will be used as waiting time for the users
    tasks = {bbbTaskSet:1, scTaskSet:3, docTaskSet:1, reqWithoutUserTaskSet:1, rocketChatTaskSet:1} # Conatins all task-sets which will be applied on the users
    MATRIX_MESSENGER = os.environ.get("MMHOST")
    timeToWaitShort = int(os.environ.get("TIMESHORT"))
    timeToWaitLong = int(os.environ.get("TIMELONG"))
    returncodeNormal = 200 # Returncode if a Request is successful
    returncodeRedirect = 302 # Returncode if a Request is successful and the user was redirected on an other website
    returncodeCreated = 201 # Returncode if a Request to create something was successful
    bBBKey = os.environ.get("BBBKEY")
    bBBHost = os.environ.get("BBBHOST")
    numberRooms = int(os.environ.get("BBBNUMBERROOMS"))
    numberUsers = int(os.environ.get("BBBNUMBERUSERS"))
    urlBetterMarks = os.environ.get("URLBETTERMARKS") # required for downloading bettermarks-tools

    # Get the user credentials for locust HttpUser. Either the file-path or the constants will be used, other wise the programm will exit.
    userCredentialsFilePath = os.environ.get("USER_CREDENTIALS_FILE_PATH")
    loginCredentialsAdmin = {'email':os.environ.get("ADMIN_EMAIL"), 'password':os.environ.get("ADMIN_PASSWORD")}
    loginCredentialsTeacher = {'email':os.environ.get("TEACHER_EMAIL"), 'password':os.environ.get("TEACHER_PASSWORD")}
    loginCredentialsPupil = {'email':os.environ.get("PUPIL_EMAIL"), 'password':os.environ.get("PUPIL_PASSWORD")}
