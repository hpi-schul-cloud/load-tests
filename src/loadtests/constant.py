import os

from locust import between

class constant():
    wait_time = between(5, 15) # Provides a random number which will be used as waiting time for the users
    MATRIX_MESSENGER = os.environ.get("MMHOST")
    
    if os.environ.get("TIMESHORT") is not None:
        timeToWaitShort = int(os.environ.get("TIMESHORT"))
    else:
        print(f"\n#### ALTERNATIV 1 ####\n")
        timeToWaitShort = 5
    
    if os.environ.get("TIMELONG") is not None:
        timeToWaitShort = int(os.environ.get("TIMELONG"))
    else:
        print(f"\n#### ALTERNATIV 2 ####\n")
        timeToWaitShort = 10

    returncodeNormal = 200 # Returncode if a Request is successful
    returncodeRedirect = 302 # Returncode if a Request is successful and the user was redirected on an other website
    returncodeCreated = 201 # Returncode if a Request to create something was successful
    bBBKey = os.environ.get("BBBKEY")
    bBBHost = os.environ.get("BBBHOST")
    
    if os.environ.get("BBBNUMBERROOMS") is not None:
        timeToWaitShort = int(os.environ.get("BBBNUMBERROOMS"))
    else:
        print(f"\n#### ALTERNATIV 3 ####\n")
        timeToWaitShort = 3
    
    if os.environ.get("BBBNUMBERUSERS") is not None:
        timeToWaitShort = int(os.environ.get("BBBNUMBERUSERS"))
    else:
        print(f"\n#### ALTERNATIV 4 ####\n")
        timeToWaitShort = 6

    urlBetterMarks = os.environ.get("URLBETTERMARKS") # required for downloading bettermarks-tools

    # Get the user credentials for locust HttpUser. Either the file-path or the constants will be used, other wise the programm will exit.
    userCredentialsFilePath = os.environ.get("USER_CREDENTIALS_FILE_PATH")
    loginCredentialsAdmin = {'email':os.environ.get("ADMIN_EMAIL"), 'password':os.environ.get("ADMIN_PASSWORD")}
    loginCredentialsTeacher = {'email':os.environ.get("TEACHER_EMAIL"), 'password':os.environ.get("TEACHER_PASSWORD")}
    loginCredentialsPupil = {'email':os.environ.get("PUPIL_EMAIL"), 'password':os.environ.get("PUPIL_PASSWORD")}
