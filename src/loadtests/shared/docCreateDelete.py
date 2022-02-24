import time
import requests

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By

from loadtests.shared.constant import Constant
from loadtests.loadtests.functions import requestHeaderBuilder


def newFilesDocxShared(session):
        '''
        Task for creating and editing .docx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document.
        Deletes the doument after finishing the task.
        '''

        if session._user.user_type == "pupil":
            pass
        else:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name"          : "Loadtest docx",
                "type"          : "docx",
                "studentEdit"   : "false"
            }

            # Creates .docx document
            docId = createDoc(session, data) # ID of the new document
            session.createdDocuments.append(docId)
            print(docId)

            host = session.user.host + "/files" # url to where the file will be saved

            driverWB = webdriver.Remote(f"http://{Constant.browserIpPort}/wd/hub", DesiredCapabilities.CHROME) # browser which will be used for calling the host and saving the documents
            driverWB.get(host)

            # Login user
            ui_element = "input[id='name']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(session.user.login_credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(session.user.login_credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = f"{session.user.host}/files/file/{docId}/lool"
            driverWB.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.TAG_NAME, ui_element)))
            driverWB.switch_to.frame(element)
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.TAG_NAME, ui_element)))
            driverWB.switch_to.frame(element)

            time.sleep(int(Constant.timeToWaitShort))

            # Edit document
            ui_element = "html/body"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.XPATH, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")

            time.sleep(int(Constant.timeToWaitShort))

            driverWB.quit()
            deleteDoc(session, docId)
            return docId
            
def newFilesXlsxShared(session):
        '''
        Task for creating and editing .xlsx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document.
        Deletes the doument after finishing the task.
        '''

        if session._user.user_type == "pupil":
            pass
        else:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name"          : "Loadtest xlsx",
                "type"          : "xlsx",
                "studentEdit"   : "false"
            }

            # Creates .xlsx document
            docId = createDoc(session, data) # ID of the new document
            session.createdDocuments.append(docId)

            host = session.user.host + "/files" # url to where the file will be saved

            driverWB = webdriver.Remote(f"http://{Constant.browserIpPort}/wd/hub", DesiredCapabilities.CHROME)
            #driverWB = webdriver.Chrome(executable_path=self.workpath + '/chromedriver') # browser which will be used for calling the host and saving the documents
            driverWB.get(host)

            # Login User
            ui_element = "input[id='name']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(session.user.login_credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(session.user.login_credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = session.user.host + "/files/file/" + docId + "/lool"
            driverWB.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.TAG_NAME, ui_element)))
            driverWB.switch_to.frame(element)

            time.sleep(int(Constant.timeToWaitShort))

            # Edit Doc
            ui_element = "input[id='formulaInput']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")
            ui_element = "td[id='tb_editbar_item_save']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            time.sleep(int(Constant.timeToWaitShort))

            driverWB.quit()
            deleteDoc(session, docId)
            return docId

def newFilesPptxShared(session):
        '''
        Task for creating and editing .pptx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document.
        Deletes the doument after finishing the task.
        '''

        if session._user.user_type == "pupil":
            pass
        else:
            # provides the post-request (for saving the created document) with necessary informations
            data = {
                "name"          : "Loadtest pptx",
                "type"          : "pptx",
                "studentEdit"   : "false"
            }

            # Create .pptx document
            docId = createDoc(session, data) # ID of the new document
            session.createdDocuments.append(docId)

            host = session.user.host + "/files" # url to where the file will be saved

            driverWB = webdriver.Remote(f"http://{Constant.browserIpPort}/wd/hub", DesiredCapabilities.CHROME)
            #driverWB = webdriver.Chrome(executable_path=self.workpath + '/chromedriver') # browser which will be used for calling the host and saving the documents
            driverWB.get(host)

            # Login User
            ui_element = "input[id='name']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(session.user.login_credentials["email"])

            ui_element = "input[id='password']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.send_keys(session.user.login_credentials["password"])

            ui_element = "input[id='submit-login']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            element.click()

            host = f"{session.user.host}/files/file/{docId}/lool"
            driverWB.get(host)

            # Switch to editorframe
            ui_element = "iframe"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.TAG_NAME, ui_element)))
            driverWB.switch_to.frame(element)
            ui_element = "iframe[class='resize-detector']"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ui_element)))
            driverWB.switch_to.frame(element)

            time.sleep(int(Constant.timeToWaitShort))

            # Edit Doc
            ui_element = "html/body"
            element = WebDriverWait(driverWB, 15).until(EC.presence_of_element_located((By.XPATH, ui_element)))
            element.send_keys("Der Loadtest der loaded den Test!")

            time.sleep(int(Constant.timeToWaitShort))

            driverWB.quit()
            deleteDoc(session, docId)
            return docId

def createDoc(session, docdata):
    '''
    Creates a document on the SchulCloud website.

    Param:
        self: Taskset
        docdata: Configuration for the new Document
    '''
    header = requestHeaderBuilder(session, "/files/my/")
    header["Content-Type"] = "application/x-www-form-urlencoded" # Adding entry "Content-Type" (data format for request body)

    with session.client.post("/files/my", 
        data = docdata,
        #ContentTypeHeader = "application/x-www-form-urlencoded" # Adding entry "Content-Type" (data format for request body),
    ) as response:
        if response.status_code != Constant.returncodeNormal:
            print(response.failure())#requestFailureMessage(self, response))
        else:
            session.createdDocuments.append(response.text) # Adding the new document to createdDocumets-list for final clean-up
            return response.text

def deleteDoc(session, docId):
    '''
    Deletes a document on the SchulCloud website.

    Param:
        self: Taskset
        docId: Document ID
    '''
    data = {"id" : docId}
    header = {
        "Connection"        : "keep-alive", # 'keep-alive' allows the connection to remain open for further requests/response
        "x-requested-with"  : "XMLHttpRequest", # Used for identifying Ajax requests
        "csrf-token"        : session.cookies['csrftoken'], # Security token
        "Origin"            : session.host,
        "Sec-Fetch-Site"    : "same-origin", # Indicates the origin of the request
        "Sec-Fetch-Mode"    : "cors", # Indicates the mode of the request
        "Sec-Fetch-Dest"    : "empty", # Indicates the request's destination
        "Referer"           : f"{session.host}/files/my/"
    }

    with session.client.delete(
        "/files/file/",
        headers = header,
        data = data,
        catch_response = True,
        allow_redirects = True,
        name="/files/file/delete"
    ) as response:
        if response.status_code != Constant.returncodeNormal:
            print(response.failure())