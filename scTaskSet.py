import locustfile

from loginout import *
from requestsBuilder import *
from locust.user.task import TaskSet, tag
from locust import task 

class scTaskSet(TaskSet):
    '''
    Definition of the specific tasks, the loadtest should execute.
    Tasks, which are marked with tags, can be directly addressed by the start of the loadtest. The other tasks then will be ignored.

    Args:
        Lists which contain all the doc/courses/teams ID's beeing created from the loadtest.
        All three lists are necessary for a clean log-out procress in 'loginout'.
    '''

    # Lists which contain all the doc/courses/teams ID's beeing created from the loadtest.
    # All three lists are necessary for a clean log-out procress in 'loginout'.
    createdDocuments = []
    createdCourses = []
    createdTeams = []

    def on_start(self):
        '''
        Frist Task that is executed.
        It logs in the User.

        Param:
            self: Taskset 
        '''
        login(self)

    def on_stop(self):
        '''
        Last Task that is executed.
        It cleans up courses, teams and documents and logs the user out.

        Param:
            self: Taskset
        '''
        logout(self)

    @tag('sc')
    @task
    def index(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.
        Param:
            self: Taskset
        '''
        normalGET(self, "/")

    @tag('sc')
    @task
    def calendar(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/calendar/")

    @tag('sc')
    @task
    def account(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/account/")

    @tag('sc')
    @task
    def dashboard(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/dashboard/")

    @tag('sc')
    @task
    def courses(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/courses/")

    @tag('sc')
    @task
    def courses_add(self):
        '''
        If the user isnt a PupilUser, it starts a Get-Request to the hand over URL

        Param:
            self: Taskset
        '''
        if isinstance(self._user, locustfile.PupilUser):
           pass
        else:
            normalGET(self, "/courses/add/")

    @tag('sc')
    @task
    def homework(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/homework/")

    @tag('sc')
    @task
    def homework_new(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/homework/new/")

    @tag('sc')
    @task
    def homework_asked(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.
        Param:
            self: Taskset
        '''
        normalGET(self, "/homework/asked/")

    @tag('sc')
    @task
    def homework_private(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/homework/private/")

    @tag('sc')
    @task
    def homework_archive(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/homework/archive/")

    @tag('sc')
    @task
    def files(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/files/")

    @tag('sc')
    @task
    def files_my(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/files/my/")

    @tag('sc')
    @task
    def files_courses(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/files/courses/")

    @tag('sc')
    @task
    def files_shared(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/files/shared/")

    @tag('sc')
    @task
    def files_shared(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.
        Param:
            self: Taskset
        '''
        normalGET(self, "/files/shared/")

    @tag('sc')
    @task
    def news(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/news/")

    @tag('sc')
    @task
    def newsnew(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/news/new")

    @tag('sc')
    @task
    def addons(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.
        Param:
            self: Taskset
        '''
        normalGET(self, "/addons/")

    @tag('sc')
    @task
    def content(self):
        '''
        Task that starts a Get-Request-Function to the hand over URL.

        Param:
            self: Taskset
        '''
        normalGET(self, "/content/")

    @tag('sc')
    @tag('course')
    @task
    def courses_add_Lernstore(self):
        '''
        Task that, if the user is not a PupilUser, starts the function
        lernstore.

        Param:
            self: Taskset
        '''
        if isinstance(self._user, locustfile.PupilUser):
           pass
        else:
            lernStore(self)

    @tag('sc')
    @tag('course')
    @task
    def courses_add_course(self):
        '''
        Task that, if the user is not a PupilUser, starts the function
        courseAddEtherPadAndTool.

        Param:
            self: Taskset
        '''
        if isinstance(self._user, locustfile.PupilUser):
           pass
        else:
            courseAddEtherPadAndTool(self)
    
    @tag('test')
    @tag('sc')
    @task
    def createDeleteTeam(self):
        '''
        Task that, if the user is not a PupilUser, starts the function
        createDeleteTeam.

        Param:
            self: Taskset
        '''
        if isinstance(self._user, locustfile.PupilUser):
          pass
        else:
            createDeleteTeam(self)

    @tag('mm')
    @task
    def message(self):
        '''
        Task that, if the user is not a PupilUser, starts the function
        MatrixMessenger.

        Param:
            self: Taskset
        '''
        # Posts and edits messages at the Matrix Messenger
        if isinstance(self._user, locustfile.PupilUser):
           pass
        else:
            matrixMessenger(self)