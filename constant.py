import os

from bbbTaskSet import *
from scTaskSet import *
from docTaskSet import *
from locust import between

class constant():
    wait_time = between(5, 15) # Provides a random number which will be used as waiting time for the users
    tasks = {bbbTaskSet:1, scTaskSet:5, docTaskSet:1} # Conatins all task-sets which will be applied on the users
    matrixMessengerHost = os.environ.get("MMHOST")
    timeToWaitShort = int(os.environ.get("TIMESHORT"))
    timeToWaitLong = int(os.environ.get("TIMELONG"))
    returncodeNormal = 200 # Returncode if a Request is successful
    returncodeRedirect = 302 # Returncode if a Request is successful and the user was redirected on an other website
    returncodeCreated = 201 # Returncode if a Request to create something was successful
    bBBKey = os.environ.get("BBBKEY")
    bBBHost = os.environ.get("BBBHOST")
    numberRooms = 3 #int(os.environ.get("BBBNUMBERROOMS"))
    numberUsers = 6 #int(os.environ.get("BBBNUMBERUSERS"))