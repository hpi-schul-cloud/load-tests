
from loadtests.shared.loadEnv import getEnvironmentVariable, checkForMissingEnvironmentVariables

MATRIX_MESSENGER = getEnvironmentVariable("MMHOST")

timeToWaitShort = int(getEnvironmentVariable("TIMESHORT"))
timeToWaitLong = int(getEnvironmentVariable("TIMELONG"))
numberRooms = int(getEnvironmentVariable("BBBNUMBERROOMS"))
numberUsers = int(getEnvironmentVariable("BBBNUMBERUSERS"))

adminWeight = int(getEnvironmentVariable("ADMIN_WEIGHT"))
teacherWeight = int(getEnvironmentVariable("TEACHER_WEIGHT"))
pupilWeight = int(getEnvironmentVariable("PUPIL_WEIGHT"))
anonymousWeight = int(getEnvironmentVariable("ANONYMOUS_WEIGHT"))

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
