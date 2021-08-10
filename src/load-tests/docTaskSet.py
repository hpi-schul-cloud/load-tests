import time
import locustfile
import constant

from loginout import *
from functions import createDoc, deleteDoc
from locust.user.task import TaskSet, task, tag
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By

class docTaskSet(TaskSet):
    '''
    Task-Set which contains all test-tasks for working with documents on the SchulCloud.
    '''

    # Lists which contain all the doc/courses/teams ID's beeing created from the loadtest. 
    # All three lists are necessary for a clean log-out procress in 'loginout'.
    createdDocuments = []
    createdCourses = []
    createdTeams = []

    def on_start(self):
        '''
        First task on docTaskSet, which starts the login of the user.
        '''
        login(self)

    def on_stop(self):
        '''
        Last task on docTaskSet, which will be triggerd after stopping the loadtest. Automatically starts a clean-up and loggs out the user.
        '''
        logout(self)

    @tag('doc')
    @tag('sc')
    @task
    def newFilesDocx(self):
        '''
        Task for creating and editing .docx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document. 
        Deletes the doument after finishing the task.
        '''

        if isinstance(self._user, locustfile.PupilUser):
            pass
        else:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name"          : "Loadtest docx",
                "type"          : "docx",
                "studentEdit"   : "false"
            }
            
            # Creates .docx document
            docId = createDoc(self, data) # ID of the new document
            self.createdDocuments.append(docId)

            host = self.user.host + "/files" # url to where the file will be saved

            driverWB = webdriver.Chrome('.\chromedriver.exe') # browser which will be used for calling the host and saving the documents
            driverWB.get(host)

            # Login user
            ui_element = "input[id='name']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.login_credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.login_credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = self.user.host + "/files/file/" + docId + "/lool"
            driverWB.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.TAG_NAME, ui_element)))
            driverWB.switch_to.frame(element)
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.TAG_NAME, ui_element)))
            driverWB.switch_to.frame(element)

            time.sleep(constant.constant.timeToWaitShort)

            # Edit document
            ui_element = "html/body"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.XPATH, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")

            time.sleep(constant.constant.timeToWaitShort)

            driverWB.quit()
            deleteDoc(self, docId)

    @tag('doc')
    @tag('sc')
    @task
    def newFilesXlsx(self):
        '''
        Task for creating and editing .xlsx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document. 
        Deletes the doument after finishing the task.
        '''

        if isinstance(self._user, locustfile.PupilUser):
            pass
        else:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name"          : "Loadtest xlsx",
                "type"          : "xlsx",
                "studentEdit"   : "false"
            }
            
            # Creates .xlsx document
            docId = createDoc(self, data) # ID of the new document
            self.createdDocuments.append(docId)

            host = self.user.host + "/files" # url to where the file will be saved

            driverWB = webdriver.Chrome('.\chromedriver.exe') # browser which will be used for calling the host and saving the documents
            driverWB.get(host)

            # Login User
            ui_element = "input[id='name']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.login_credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.login_credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = self.user.host + "/files/file/" + docId + "/lool"
            driverWB.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.TAG_NAME, ui_element)))
            driverWB.switch_to.frame(element)

            time.sleep(constant.constant.timeToWaitShort)

            # Edit Doc
            ui_element = "input[id='formulaInput']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")
            ui_element = "td[id='tb_editbar_item_save']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(constant.constant.timeToWaitShort)

            driverWB.quit()
            deleteDoc(self, docId)

    @tag('doc')
    @tag('sc')
    @task
    def newFilesPptx(self):
        '''
        Task for creating and editing .pptx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document. 
        Deletes the doument after finishing the task.
        '''

        if isinstance(self._user, locustfile.PupilUser):
            pass
        else:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name"          : "Loadtest pptx",
                "type"          : "pptx",
                "studentEdit"   : "false"
            }
            
            # Create .pptx document
            docId = createDoc(self, data) # ID of the new document
            self.createdDocuments.append(docId)

            host = self.user.host + "/files" # url to where the file will be saved

            driverWB = webdriver.Chrome('.\chromedriver.exe') # browser which will be used for calling the host and saving the documents
            driverWB.get(host)

            # Login User
            ui_element = "input[id='name']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.login_credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(self.user.login_credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = self.user.host + "/files/file/" + docId + "/lool"
            driverWB.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.TAG_NAME, ui_element)))
            driverWB.switch_to.frame(element)
            ui_element = "iframe[class='resize-detector']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            driverWB.switch_to.frame(element)

            time.sleep(constant.constant.timeToWaitShort)

            # Edit Doc
            ui_element = "html/body"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.XPATH, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")

            time.sleep(constant.constant.timeToWaitShort)

            driverWB.quit()
            deleteDoc(self, docId)