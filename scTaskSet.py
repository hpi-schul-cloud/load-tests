from loginout import *
from requestsBuilder import *
from locust.user.task import TaskSet, tag
from locust import task 

class scTaskSet(TaskSet):

    def on_start(self):
        self = login(self)

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

    @tag('test')
    @tag('sc')
    @task
    def courses_add(self):
        #if isinstance(self._user, PupilUser.__class__):
        #    pass
        #else:
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

    @tag('test')
    @tag('sc')
    @tag('course')
    @task
    def courses_add_Lernstore(self):
        #if isinstance(self._user, Locustfile.PupilUser):
        #    pass
        #else:
        lernStore(self)

    @tag('sc')
    @tag('course')
    @task
    def courses_add_course(self):
        #if isinstance(self._user, Locustfile.PupilUser):
        #    pass
        #else:
        courseAddEtherPadAndTool(self)
    
    @tag('sc')
    @task
    def newTeam(self):
        #if isinstance(self._user, Locustfile.PupilUser):
        #   pass
        #else:
        newTeam(self)

    @tag('mm')
    @task
    def message(self):
        
        # Posts and edits messages at the Matrix Messenger
        #if isinstance(self._user, Locustfile.PupilUser):
        #    pass
        #else:
        matrixMessenger(self)