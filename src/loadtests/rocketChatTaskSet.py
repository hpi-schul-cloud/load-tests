from loadtests import functions
from loadtests import loginout
import time
import os
import shutil
import urllib.request

from locust.user.task import TaskSet, tag, task
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class rocketChatTaskSet(TaskSet):
    '''
    This class defines the TaskSet for RocketChat.
    '''

    # Lists which contain all the doc/courses/teams ID's beeing created from the loadtest.
    # All three lists are necessary for a clean log-out process in 'loginout'.
    createdDocuments = []
    createdCourses = []
    createdTeams = []

    # Initialization of important id's
    school_id = None
    user_id = None

    def on_start(self):
        loginout.login(self)
        remote_url = 'https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip'
        # Define the local filename to save data
        local_file = 'chromedriver_linux64.zip'
        # Download remote and save locally
        urllib.request.urlretrieve(remote_url, local_file)
        shutil.unpack_archive(local_file)

    def on_stop(self):
        if os.path.exists("chromedriver.exe"):
            os.remove("chromedriver.exe")
        loginout.logout(self)

    @tag('rocketChat')
    @task
    def createTeamWithRocketChat(self):
        '''
        This task creates a new team and enables the team-messenger (settings). Afterwards, it opens the team-messenger and
        posts some chat messanges. At the end, the created team will be deleted.

        Note: Only teacher or admins can create a new team. Because there are many bugs on enabling RocketChat for a team on the SchulCloud,
        this method contains several workarounds.

        Param:
        - self (TaskSet) : TaskSet for RocketChat
        '''

        if self._user.user_type != "pupil":
            teamId = functions.newTeam(self)

            # Opens chrome browser
            url = f"{self.user.host}/teams/{teamId}/edit"
            driverWB = webdriver.Chrome(executable_path='./chromedriver') # browser which will be used
            driverWB.get(url)

            functions.loginLoadtestUserOnTeamToEdit(self, driverWB) # Login user
            functions.enableTeamMessenger(driverWB) # Enable team messenger

            # Open team chat in new tab (RocketChat)
            url = f"https://chat.{self.user.host.replace('https://', '')}/group/{functions.findTeamChatId(self, teamId)}"
            driverWB.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') # Open new tab
            time.sleep(1)
            driverWB.get(url)
            time.sleep(1)

            functions.postTeamChatMessage(self, driverWB) # Post messages

            driverWB.close # Close webbrowser

