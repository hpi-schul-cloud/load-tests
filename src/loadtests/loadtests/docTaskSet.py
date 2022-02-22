import time

from locust.user.task import TaskSet, task, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By

from loadtests.shared.constant import Constant
from loadtests.loadtests import loginout
from loadtests.loadtests.functions import createDoc, deleteDoc
from loadtests.shared.docCreateDelete import newFilesDocxShared, newFilesPptxShared, newFilesXlsxShared

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
        loginout.login(self)
        loginout.installChromedriver(self)

    def on_stop(self):
        '''
        Last task on docTaskSet, which will be triggerd after stopping the loadtest. Automatically starts a clean-up and loggs out the user.
        '''
        loginout.deleteChromedriver(self)
        loginout.logout(self)

    @tag('doc')
    @task
    def newFilesDocx(self):
        '''
        Task for creating and editing .docx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document.
        Deletes the doument after finishing the task.
        '''
        self.createdDocuments.append(newFilesDocxShared(self.session))
        

    @tag('doc')
    @task
    def newFilesXlsx(self):
        '''
        Task for creating and editing .xlsx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document.
        Deletes the doument after finishing the task.
        '''
        self.createdDocuments.append(newFilesXlsxShared(self.session))

        
    @tag('doc')
    @task
    def newFilesPptx(self):
        '''
        Task for creating and editing .pptx documents on the SchulCloud.

        Abbords, if the user is a pupil user. Otherwise, logs in the user and creates as well as edits a new document.
        Deletes the doument after finishing the task.
        '''
        self.createdDocuments.append(newFilesPptxShared(self.session))