import time
import os
import hashlib
import constant

from locust import task, tag
from locust.user.task import TaskSet
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException, NoSuchWindowException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By

class bbbTaskSet(TaskSet):
    '''
    Task-Set which contains all test-tasks for working with BBB on the SchulCloud.

    Args:
        bBBKey (str) : key for using BBB
        bBBHost (str) : url of BBB
        numberRooms (int) : number of rooms which should be created
        numberUsers (int) : number od useres which are involved in the test
        timeWaitShort (int) : waiting time short
        timeWaitLong (int) : waiting time long
    '''

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @tag('bbb')
    @task
    def bBBTest(self):
        '''
        Task for creating multiple BBB rooms.

        Creates the number of BBB rooms which is contained in the 'numberRooms' variable. After creating a room, other users join and the 
        moderator will share a video. The number of joining users is contained in the 'numberUsers' variable. After finishing the taks, all tabs
        and BBB rooms will be closed.

        Args:
            driverWB (webdriver) : browser which will be used for creating the BBB rooms
            counterfirst (int) : counter for creating a specific number of rooms
            countersecond (int) : counter for users to join a BBB room
            counterTab (int) : counter for open tabs
        '''

        #Starts a chrome Browser
        driverWB = webdriver.Chrome('.\chromedriver.exe')
        driverWB.get(constant.constant.bBBHost)

        counterfirst = 0
        counterTab = 1
        while counterfirst < constant.constant.numberRooms:

            timestamp = str(time.time())
            # Creates a BBB-Room with a password
            operator = "create"
            urlparam = "meetingID=loadtest-" + timestamp + str(counterfirst) + "&name=loadtest-" + str(time.time()) + str(counterfirst) + "&moderatorPW=123&attendeePW=456&lockSettingsDisableMic=true"
            urlstart = constant.constant.bBBHost + "/bigbluebutton/api/" + operator + "?" + urlparam
            url = str(operator) + str(urlparam) + str(constant.constant.bBBKey)
            urlsha = str(urlstart) + "&checksum=" + hashlib.sha1(url.encode()).hexdigest()

            driverWB.get(urlsha)

            countersecond = 0

            # Moderator joins the room on a new Tab
            operator = "join"
            urlparam = "meetingID=loadtest-" + timestamp + str(counterfirst) + "&fullName=loadtest-" + str(counterfirst) + "userMLoadtest-" + str(countersecond) + "&userID=loadtest-" + str(counterfirst) + "userMLoadtest-" + str(countersecond) + "&password=123"
            urlstart = constant.constant.bBBHost + "/bigbluebutton/api/" + operator + "?" + urlparam
            url = str(operator) + str(urlparam) + str(constant.constant.bBBKey)
            urlsha = urlstart + "&checksum=" + hashlib.sha1(url.encode()).hexdigest()

            windows = driverWB.window_handles
            driverWB.execute_script("window.open('');")
            driverWB.switch_to.window(driverWB.window_handles[counterTab])
            driverWB.get(urlsha)
            # time.sleep(self.timeToWaitShort)

            # Chooses to join the room with "Listen only"
            ui_element = "i[class='icon--2q1XXw icon-bbb-listen']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(constant.constant.timeToWaitShort)

            # Clicks on the Plussign
            ui_element = "tippy-21"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.ID, ui_element)))
            element.click()

            # Clicks on the "Share external Video" button
            ui_element = "li[aria-labelledby='dropdown-item-label-26']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            # Inserts Videolink
            ui_element = "input[id='video-modal-input']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys('https://player.vimeo.com/video/418854539')

            time.sleep(constant.constant.timeToWaitShort)

            # Clicks on the button "Share a new video"
            ui_element = "button[class='button--Z2dosza md--Q7ug4 default--Z19H5du startBtn--ZifpQ9']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(constant.constant.timeToWaitLong)

            counterTab += 1
            countersecond += 1

            while countersecond < constant.constant.numberUsers:

                # Normal User joins the room
                operator = "join"
                urlparam = "meetingID=loadtest-" + timestamp + str(counterfirst) + "&fullName=loadtest-" + str(counterfirst) + "userLoadtest-" + str(countersecond) + "&userID=loadtest-" + str(counterfirst) + "userLoadtest-" + str(countersecond) + "&password=456"
                urlstart = constant.constant.bBBHost + "/bigbluebutton/api/" + operator + "?" + urlparam
                url = str(operator) + str(urlparam) + str(constant.constant.bBBKey)
                urlsha = urlstart + "&checksum=" + hashlib.sha1(url.encode()).hexdigest()

                # changes the browsertab
                windows = driverWB.window_handles
                driverWB.execute_script("window.open('');")
                driverWB.switch_to.window(driverWB.window_handles[counterTab])
                driverWB.get(urlsha)

                ui_element = "button[aria-label='Play audio']"
                element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
                element.click()

                time.sleep(constant.constant.timeToWaitLong)

                countersecond += 1
                counterTab += 1

            counterfirst += 1

        counterfirst = 0
        time.sleep(30)
        while counterfirst < constant.constant.numberRooms:
            # Closes all the rooms
            operator = "end"
            urlparam = "meetingID=loadtest-" + timestamp + str(counterfirst) + "&password=123"
            urlstart = constant.constant.bBBHost + "/bigbluebutton/api/" + operator + "?" + urlparam
            url = str(operator) + str(urlparam) + str(constant.constant.bBBKey)
            urlsha = str(urlstart) + "&checksum=" + hashlib.sha1(url.encode()).hexdigest()

            driverWB.get(urlsha)

            time.sleep(2)
            counterfirst += 1

        driverWB.quit()