import os
import logging

from locust import between

class constant():
    logger = logging.getLogger(__name__)
    
    wait_time = between(5, 15) # Provides a random number which will be used as waiting time for the users
    MATRIX_MESSENGER = os.environ.get("MMHOST")
    
    timeToWaitShort = int(os.getenv("TIMESHORT", 5))
    logger.info(timeToWaitShort)
    timeToWaitLong = int(os.getenv("TIMELONG", 10))
    logger.info(timeToWaitLong)
    numberRooms = int(os.getenv("BBBNUMBERROOMS", 3))
    logger.info(numberRooms)
    numberUsers = int(os.getenv("BBBNUMBERUSERS", 6))
    logger.info(numberUsers)

    adminWeight = int(os.getenv("ADMIN_WEIGHT", 1))
    logger.info(adminWeight)
    teacherWeight = int(os.getenv("TEACHER_WEIGHT", 3))
    logger.info(teacherWeight)
    pupilWeight = int(os.getenv("PUPIL_WEIGHT", 5))
    logger.info(pupilWeight)
    anonymousWeight = int(os.getenv("ANONYMOUS_WEIGHT", 10))
    logger.info(anonymousWeight)

    returncodeNormal = 200 # Returncode if a Request is successful
    returncodeRedirect = 302 # Returncode if a Request is successful and the user was redirected on an other website
    returncodeCreated = 201 # Returncode if a Request to create something was successful
    
    bBBKey = os.environ.get("BBBKEY")
    bBBHost = os.environ.get("BBBHOST")

    browserIpPort= os.getenv("BROWSERIPPORT", "chromedriver-svc:4444") #URL and Port for the chromedriver Pod

    urlBetterMarks = os.environ.get("URLBETTERMARKS") # required for downloading bettermarks-tools

    # Get the user credentials for locust HttpUser. Either the file-path or the constants will be used, other wise the programm will exit.
    userCredentialsFilePath = os.environ.get("USER_CREDENTIALS_FILE_PATH")
    loginCredentialsAdmin = {'email':os.environ.get("ADMIN_EMAIL"), 'password':os.environ.get("ADMIN_PASSWORD")}
    loginCredentialsTeacher = {'email':os.environ.get("TEACHER_EMAIL"), 'password':os.environ.get("TEACHER_PASSWORD")}
    loginCredentialsPupil = {'email':os.environ.get("PUPIL_EMAIL"), 'password':os.environ.get("PUPIL_PASSWORD")}
