
import time
import hashlib

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions  # available since 2.26.0
from selenium.webdriver.common.by import By
from locust.user.task import TaskSet

from loadtests.loadtests.config import Config
from loadtests.loadtests.chromedriver_download import asure_chromedriver


asure_chromedriver()


class TasksetBBB(TaskSet):
    """
    Task-Set which contains all test-tasks for working with BBB on the SchulCloud.
    """

    #@tag('bbb')
    #@task
    def test(self):
        """
        Task for creating multiple BBB rooms.

        Creates the number of BBB rooms which is contained in the 'numberRooms' variable. After creating a room, other users join and the
        moderator will share a video. The number of joining users is contained in the 'numberUsers' variable. After finishing the taks, all tabs
        and BBB rooms will be closed.
        """

        self.shared_test()

    def shared_test(self):
        """
        Task for creating multiple BBB rooms.

        Creates the number of BBB rooms which is contained in the 'numberRooms' variable. After creating a room, other users join and the
        moderator will share a video. The number of joining users is contained in the 'numberUsers' variable. After finishing the taks, all tabs
        and BBB rooms will be closed.
        """

        # TODO: get bbb host and key (previously configured via env vars)

        bbb_host = None
        bbb_key = None
        raise NotImplementedError()

        # Starts a chrome Browser
        driver_wb = webdriver.Remote(f"http://{Config.BROWSER_IP_PORT}/wd/hub",
                                     DesiredCapabilities.CHROME)
        driver_wb.get(bbb_host)

        room_count = 0
        tab_count = 1
        while room_count < int(Config.BBB_ROOM_COUNT):

            timestamp = str(time.time())
            # Creates a BBB-Room with a password
            operator = "create"
            urlparam = f"meetingID=loadtest-{timestamp}{str(room_count)}&name=loadtest-{str(time.time())}{str(room_count)}&moderatorPW=123&attendeePW=456&lockSettingsDisableMic=true"
            urlstart = bbb_host + "/bigbluebutton/api/" + operator + "?" + urlparam
            url = str(operator) + str(urlparam) + str(bbb_key)
            urlsha = f"{str(urlstart)}&checksum={hashlib.sha1(url.encode()).hexdigest()}"

            driver_wb.get(urlsha)

            user_count = 0

            # Moderator joins the room on a new Tab
            operator = "join"
            urlparam = f"meetingID=loadtest-{timestamp}{str(room_count)}&fullName=loadtest-{str(room_count)}userMLoadtest-{str(user_count)}&userID=loadtest-{str(room_count)}userMLoadtest-{str(user_count)}&password=123"
            urlstart = f"{bbb_host}/bigbluebutton/api/{operator}?{urlparam}"
            url = str(operator) + str(urlparam) + str(bbb_key)
            urlsha = f"{urlstart}&checksum={hashlib.sha1(url.encode()).hexdigest()}"

            windows = driver_wb.window_handles
            driver_wb.execute_script("window.open('');")
            driver_wb.switch_to.window(driver_wb.window_handles[tab_count])
            driver_wb.get(urlsha)
            # time.sleep(self.timeToWaitShort)

            # Chooses to join the room with "Listen only"
            ui_element = "i[class='icon--2q1XXw icon-bbb-listen']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(int(Config.WAIT_TIME_SHORT))

            # Clicks on the Plussign
            ui_element = "tippy-19"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.ID, ui_element)))
            element.click()

            # Clicks on the "Share external Video" button
            ui_element = "li[data-test='external-video']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            # Inserts Videolink
            ui_element = "input[id='video-modal-input']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys('https://player.vimeo.com/video/418854539')

            time.sleep(int(Config.WAIT_TIME_SHORT))

            # Clicks on the button "Share a new video"
            ui_element = "button[class='button--Z2dosza md--Q7ug4 default--Z19H5du startBtn--ZifpQ9']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(int(Config.WAIT_TIME_SHORT))

            tab_count += 1
            user_count += 1

            while user_count < int(Config.BBB_USER_COUNT):
                # Normal User joins the room
                operator = "join"
                urlparam = f"meetingID=loadtest-{timestamp}{str(room_count)}&fullName=loadtest-{str(room_count)}userLoadtest-{str(user_count)}&userID=loadtest-{str(room_count)}userLoadtest-{str(user_count)}&password=456"
                urlstart = f"{bbb_host}/bigbluebutton/api/{operator}?{urlparam}"
                url = str(operator) + str(urlparam) + str(bbb_key)
                urlsha = urlstart + "&checksum=" + hashlib.sha1(url.encode()).hexdigest()

                # changes the browsertab
                windows = driver_wb.window_handles
                driver_wb.execute_script("window.open('');")
                driver_wb.switch_to.window(driver_wb.window_handles[tab_count])
                driver_wb.get(urlsha)

                ui_element = "button[aria-label='Play audio']"
                element = WebDriverWait(driver_wb, 15).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
                element.click()

                time.sleep(int(Config.WAIT_TIME_SHORT))

                user_count += 1
                tab_count += 1

            room_count += 1

        room_count = 0
        time.sleep(30)
        while room_count < int(Config.BBB_ROOM_COUNT):
            # Closes all the rooms
            operator = "end"
            urlparam = f"meetingID=loadtest-{timestamp}{str(room_count)}&password=123"
            urlstart = f"{bbb_host}/bigbluebutton/api/{operator}?{urlparam}"
            url = str(operator) + str(urlparam) + str(bbb_key)
            urlsha = f"{str(urlstart)}&checksum={hashlib.sha1(url.encode()).hexdigest()}"

            driver_wb.get(urlsha)

            time.sleep(2)
            room_count += 1
        driver_wb.quit()
