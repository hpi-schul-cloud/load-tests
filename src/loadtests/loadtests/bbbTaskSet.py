from locust import task, tag
from locust.user.task import TaskSet

from loadtests.loadtests import loginout
from loadtests.shared.bBBSessionCreateDelete import bBBSharedTest

class bbbTaskSet(TaskSet):
    '''
    Task-Set which contains all test-tasks for working with BBB on the SchulCloud.
    '''

    def on_start(self):
        loginout.installChromedriver(self)


    def on_stop(self):
        loginout.deleteChromedriver(self)

    @tag('bbb')
    @task
    def bBBTest(self):
        '''
        Task for creating multiple BBB rooms.

        Creates the number of BBB rooms which is contained in the 'numberRooms' variable. After creating a room, other users join and the
        moderator will share a video. The number of joining users is contained in the 'numberUsers' variable. After finishing the taks, all tabs
        and BBB rooms will be closed.
        '''
        bBBSharedTest(self)