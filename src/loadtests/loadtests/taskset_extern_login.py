import time

from locust.user.task import TaskSet, tag, task

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions  # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from loadtests.loadtests.config import Config
from loadtests.loadtests.chromedriver_download import asure_chromedriver
from loadtests.loadtests.constant import StatusCode

asure_chromedriver()

class TasksetExternalLogin(TaskSet):
    """
        Taskset to load test external login via IDM (ErWIn IDM, Keycloak)
    """

    @tag('extern')
    @task
    def external_log_in_and_out(self):
        """
        Do a login as external user via IDM
        """

        # Starts a chrome Browser
        driver_wb = webdriver.Remote(f"http://{Config.BROWSER_IP_PORT}/wd/hub",
                                     DesiredCapabilities.CHROME)

        # navigate to login page
        url = f"{self.user.host}/login"
        driver_wb.get(url)

        # Clicks on the OIDCMOCK login
        element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-testid='submit-oauth-login']")))
        element.click()

        # Inserts user name
        ui_element_id = "Username"
        element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.ID, ui_element_id)))
        element.send_keys(self.user.credentials["email"])

        # Inserts user password, triggers login (hit ENTER)
        ui_element_id = "Password"
        element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.ID, ui_element_id)))
        element.send_keys(self.user.credentials["password"], Keys.ENTER)

        # Open settings menu
        element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@data-testid='initials']")))

        # Keep session active for at least WAIT_TIME_LONG until settings button was found (i. e. login succeeded)
        time.sleep(int(Config.WAIT_TIME_LONG))
        element.click()

        # Click logout button
        element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//a[@data-testid='logout']")))
        element.click()

        driver_wb.quit()
