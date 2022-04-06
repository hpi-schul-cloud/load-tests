
import time

from locust.user.task import task, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions  # available since 2.26.0
from selenium.webdriver.common.by import By

from loadtests.loadtests.config import Config
from loadtests.loadtests.chromedriver_download import asure_chromedriver
from loadtests.loadtests.taskset_base import TasksetBase
from loadtests.loadtests.user_type import UserType


asure_chromedriver()


class TasksetDoc(TasksetBase):
    """
    Task-Set which contains all test-tasks for working with documents on the SchulCloud.
    """

    @tag('doc')
    @task
    def new_files_docx(self):
        if not self.user.type == UserType.PUPIL:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name": "Loadtest docx",
                "type": "docx",
                "studentEdit": "false"
            }

            # Creates .docx document
            doc_id = self.create_doc(data)  # ID of the new document
            self.all_documents.append(doc_id)

            host = f"{self.user.host}/files"  # url to where the file will be saved

            driver_wb = webdriver.Remote(f"http://{Config.BROWSER_IP_PORT}/wd/hub",
                                         DesiredCapabilities.CHROME)
            driver_wb.get(host)

            # Login user
            ui_element = "input[id='name']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = f"{self.user.host}/files/file/{doc_id}/lool"
            driver_wb.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.TAG_NAME, ui_element)))
            driver_wb.switch_to.frame(element)
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.TAG_NAME, ui_element)))
            driver_wb.switch_to.frame(element)

            time.sleep(int(Config.WAIT_TIME_SHORT))

            # Edit document
            ui_element = "html/body"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.XPATH, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")

            time.sleep(int(Config.WAIT_TIME_SHORT))

            driver_wb.quit()
            self.delete_doc(doc_id)

    @tag('doc')
    @task
    def new_files_xlsx(self):
        if not self.user.type == UserType.PUPIL:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name": "Loadtest xlsx",
                "type": "xlsx",
                "studentEdit": "false"
            }

            # Creates .xlsx document
            doc_id = self.create_doc(data)  # ID of the new document
            self.all_documents.append(doc_id)

            host = f"{self.user.host}/files"  # url to where the file will be saved

            driver_wb = webdriver.Remote(f"http://{Config.BROWSER_IP_PORT}/wd/hub", DesiredCapabilities.CHROME)
            # driver_wb = webdriver.Chrome(executable_path=self.workpath + '/chromedriver') # browser which will be used for calling the host and saving the documents
            driver_wb.get(host)

            # Login User
            ui_element = "input[id='name']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = f"{self.user.host}/files/file/{doc_id}/lool"
            driver_wb.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.TAG_NAME, ui_element)))
            driver_wb.switch_to.frame(element)

            time.sleep(int(Config.WAIT_TIME_SHORT))

            # Edit Doc
            ui_element = "input[id='formulaInput']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")
            ui_element = "td[id='tb_editbar_item_save']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(int(Config.WAIT_TIME_SHORT))

            driver_wb.quit()
            self.delete_doc(doc_id)

    @tag('doc')
    @task
    def new_files_pptx(self):
        if not self.user.type == UserType.PUPIL:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name": "Loadtest pptx",
                "type": "pptx",
                "studentEdit": "false"
            }

            # Create .pptx document
            doc_id = self.create_doc(data)  # ID of the new document
            self.all_documents.append(doc_id)

            host = f"{self.user.host}/files"  # url to where the file will be saved

            driver_wb = webdriver.Remote(f"http://{Config.BROWSER_IP_PORT}/wd/hub", DesiredCapabilities.CHROME)
            # driver_wb = webdriver.Chrome(executable_path=self.workpath + '/chromedriver')
            driver_wb.get(host)

            # Login User
            ui_element = "input[id='name']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = f"{self.user.host}/files/file/{doc_id}/lool"
            driver_wb.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.TAG_NAME, ui_element)))
            driver_wb.switch_to.frame(element)
            ui_element = "iframe[class='resize-detector']"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            driver_wb.switch_to.frame(element)

            time.sleep(int(Config.WAIT_TIME_SHORT))

            # Edit Doc
            ui_element = "html/body"
            element = WebDriverWait(driver_wb, 15).until(expected_conditions.presence_of_element_located((By.XPATH, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")

            time.sleep(int(Config.WAIT_TIME_SHORT))

            driver_wb.quit()
            self.delete_doc(doc_id)
