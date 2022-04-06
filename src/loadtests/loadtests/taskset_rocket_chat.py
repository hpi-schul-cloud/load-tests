import time

from bs4 import BeautifulSoup
from locust.user.task import tag, task
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions  # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

from loadtests.loadtests.config import Config
from loadtests.loadtests.chromedriver_download import asure_chromedriver
from loadtests.loadtests.constant import StatusCode
from loadtests.loadtests.taskset_base import TasksetBase
from loadtests.loadtests.user_type import UserType


asure_chromedriver()


class TasksetRocketChat(TasksetBase):
    """
    This class defines the TaskSet for RocketChat.
    """

    # Lists which contain all the doc/courses/teams ID's beeing created from the loadtest.
    # All three lists are necessary for a clean log-out process in 'loginout'.

    @tag('rocketChat')
    @task
    def create_team_with_rocket_chat(self):
        """
        This task creates a new team and enables the team-messenger (settings). Afterwards, it opens the team-messenger and
        posts some chat messanges. At the end, the created team will be deleted.

        Note: Only teacher or admins can create a new team. Because there are many bugs on enabling RocketChat for a team on the SchulCloud,
        this method contains several workarounds.
        """

        if not self.user.type == UserType.PUPIL:
            team_id = self.create_team()

            # Opens chrome browser
            url = f"{self.user.host}/teams/{team_id}/edit"
            driver_wb = webdriver.Remote(f"http://{Config.BROWSER_IP_PORT}/wd/hub", DesiredCapabilities.CHROME)
            driver_wb.get(url)

            self.login_loadtestuser_on_team_to_edit(driver_wb)
            self.enable_team_messenger(driver_wb)

            # Open team chat in new tab (RocketChat)
            url = f"https://chat.{self.user.host.replace('https://', '')}/group/{self.find_team_chat_id(team_id)}"
            driver_wb.find_element_by_tag_name('body').send_keys(f"{Keys.COMMAND}t")
            time.sleep(1)
            driver_wb.get(url)
            time.sleep(1)

            self.post_team_chat_message(driver_wb)

            driver_wb.close()

    def find_team_chat_id(self, team_id):
        """
        Returns the team-chat-id of the provided team.
        """

        url = f"{self.user.host}/teams/{team_id}"

        # Get team-chat-id
        with self.client.request(
            "GET",
            url,
            headers=self.request_header_builder(self.user.host),
            catch_response=True,
            allow_redirects=False
        ) as response:
            if response.status_code == StatusCode.OK:
                soup = BeautifulSoup(response.text, 'html.parser')
                team_chat_id = soup.find('iframe')['src']
                host = self.user.host.replace("https://", "")
                return team_chat_id.replace('?layout=embedded', '').replace(f"https://chat.{host}/group/", '')
            else:
                response.failure(self.request_failure_message(response))

    def login_loadtestuser_on_team_to_edit(self, webbrowser):
        """
        Logs-in a user on the 'edit-page' of a team on SchulCloud.
        """

        # Login user
        ui_element = "input[id='name']"
        element = WebDriverWait(webbrowser, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
        element.send_keys(self.user.credentials["email"])

        ui_element = "input[id='password']"
        element = WebDriverWait(webbrowser, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
        element.send_keys(self.user.credentials["password"])

        ui_element = "input[id='submit-login']"
        element = WebDriverWait(webbrowser, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
        element.click()

        time.sleep(1)

    def enable_team_messenger(self, webbrowser):
        """
        Enables the team-messenger. This will create a new chat on RocketChat. When the team will be deleted later,
        the connected rocket chat will be deleted as well. Only works with an already startet webbrowser, where the user is already logged in.
        """

        # Klick on rocket chat checkbox
        ui_element = "input[id='activateRC']"
        element = WebDriverWait(webbrowser, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
        element.click()
        time.sleep(1)

        # Apply changes
        ui_element = "button[data-testid='create_team_btn']"
        element = WebDriverWait(webbrowser, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
        element.click()
        time.sleep(1)

    def post_team_chat_message(self, webbrowser):
        """
        Posts a message on rocket chat.
        """

        # Type in the test message
        ui_element = "textarea[class='rc-message-box__textarea js-input-message']"
        element = WebDriverWait(webbrowser, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
        element.send_keys("This is an automated loadtest chat message.")

        # Klick 'send' button
        ui_element = "svg[class='rc-icon rc-input__icon-svg rc-input__icon-svg--send']"
        element = WebDriverWait(webbrowser, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
        element.click()

        time.sleep(1)
