import locustfile

from loginout import *
from requestsBuilder import *
from locust.user.task import TaskSet, tag
from locust import task 

class scTaskSet(TaskSet):
    '''
    Definition of the specific tasks, the loadtest should execute.
    Tasks, which are marked with tags, can be directly addressed by the start of the loadtest. The other tasks then will be ignored.
    '''

    # Lists which contain all the doc/courses/teams ID's beeing created from the loadtest.
    # All three lists are necessary for a clean log-out procress in 'loginout'.
    createdDocuments = []
    createdCourses = []
    createdTeams = []

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)

    @tag('sc')
    @task
    def index(self):
        normalGET(self, "/")

    @tag('sc')
    @task
    def calendar(self):
        normalGET(self, "/calendar/")

    @tag('sc')
    @task
    def account(self):
        normalGET(self, "/account/")

    @tag('sc')
    @task
    def dashboard(self):
        normalGET(self, "/dashboard/")

    @tag('sc')
    @task
    def courses(self):
        normalGET(self, "/courses/")

    @tag('sc')
    @task
    def courses_add(self):
        if isinstance(self._user, locustfile.locustfile.PupilUser):
           pass
        else:
            normalGET(self, "/courses/add/")

    @tag('sc')
    @task
    def homework(self):
        normalGET(self, "/homework/")

    @tag('sc')
    @task
    def homework_new(self):
        normalGET(self, "/homework/new/")

    @tag('sc')
    @task
    def homework_asked(self):
        normalGET(self, "/homework/asked/")

    @tag('sc')
    @task
    def homework_private(self):
        normalGET(self, "/homework/private/")

    @tag('sc')
    @task
    def homework_archive(self):
        normalGET(self, "/homework/archive/")

    @tag('sc')
    @task
    def files(self):
        normalGET(self, "/files/")

    @tag('sc')
    @task
    def files_my(self):
        normalGET(self, "/files/my/")

    @tag('sc')
    @task
    def files_courses(self):
        normalGET(self, "/files/courses/")

    @tag('sc')
    @task
    def files_shared(self):
        normalGET(self, "/files/shared/")

    @tag('sc')
    @task
    def files_shared(self):
        normalGET(self, "/files/shared/")

    @tag('sc')
    @task
    def news(self):
        normalGET(self, "/news/")

    @tag('sc')
    @task
    def newsnew(self):
        normalGET(self, "/news/new")

    @tag('sc')
    @task
    def addons(self):
        normalGET(self, "/addons/")

    @tag('sc')
    @task
    def content(self):
        normalGET(self, "/content/")

    # @tag('test')
    @tag('sc')
    @tag('course')
    @task
    def courses_add_Lernstore(self):
        if isinstance(self._user, locustfile.locustfile.PupilUser):
           pass
        else:
            lernStore(self)

    @tag('sc')
    @tag('course')
    @task
    def courses_add_course(self):
        if isinstance(self._user, locustfile.locustfile.PupilUser):
           pass
        else:
            courseAddEtherPadAndTool(self)
    
    @tag('test')
    @tag('sc')
    @task
    def newTeam(self):
        if isinstance(self._user, locustfile.locustfile.PupilUser):
          pass
        else:
            newTeam(self)

    @tag('mm')
    @task
    def message(self):
        # Posts and edits messages at the Matrix Messenger
        if isinstance(self._user, locustfile.locustfile.PupilUser):
           pass
        else:
            matrixMessenger(self)