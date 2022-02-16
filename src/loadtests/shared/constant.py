import logging

from loadtests.shared.loadEnv import getEnvironmentVariable, checkForMissingEnvironmentVariables


logger = logging.getLogger(__name__)
class Constant:
    logger.error('Constant run -----------------')
    MATRIX_MESSENGER = getEnvironmentVariable("MMHOST", required=False)

    timeToWaitShort = getEnvironmentVariable("TIMESHORT", int)
    timeToWaitLong = getEnvironmentVariable("TIMELONG", int)
    numberRooms = getEnvironmentVariable("BBBNUMBERROOMS", int)
    numberUsers = getEnvironmentVariable("BBBNUMBERUSERS", int)

    adminWeight = getEnvironmentVariable("ADMIN_WEIGHT", int)
    teacherWeight = getEnvironmentVariable("TEACHER_WEIGHT", int)
    pupilWeight = getEnvironmentVariable("PUPIL_WEIGHT", int)
    anonymousWeight = getEnvironmentVariable("ANONYMOUS_WEIGHT", int)

    returncodeNormal = 200 # Returncode if a Request is successful
    returncodeRedirect = 302 # Returncode if a Request is successful and the user was redirected on an other website
    returncodeCreated = 201 # Returncode if a Request to create something was successful

    bBBKey = getEnvironmentVariable("BBBKEY")
    bBBHost = getEnvironmentVariable("BBBHOST")

    browserIpPort= getEnvironmentVariable("BROWSERIPPORT", "chromedriver-svc:4444") #URL and Port for the chromedriver Pod

    urlBetterMarks = getEnvironmentVariable("URLBETTERMARKS") # required for downloading bettermarks-tools

    # Get the user credentials for locust HttpUser. Either the file-path or the constants will be used, other wise the programm will exit.
    loginCredentialsAdmin = {'email': getEnvironmentVariable("ADMIN_EMAIL"), 'password': getEnvironmentVariable("ADMIN_PASSWORD")}
    loginCredentialsTeacher = {'email': getEnvironmentVariable("TEACHER_EMAIL"), 'password': getEnvironmentVariable("TEACHER_PASSWORD")}
    loginCredentialsPupil = {'email': getEnvironmentVariable("PUPIL_EMAIL"), 'password': getEnvironmentVariable("PUPIL_PASSWORD")}

    checkForMissingEnvironmentVariables()
