
from typing import List, Type

from loadtests.loadtests.config import Config
from loadtests.loadtests.taskset_bbb import TasksetBBB
from loadtests.loadtests.taskset_extern_login import TasksetExternalLogin
from loadtests.loadtests.taskset_schul_cloud import TasksetSchulCloud
from loadtests.loadtests.taskset_doc import TasksetDoc
from loadtests.loadtests.taskset_anonymous import TasksetAnonymous
from loadtests.loadtests.taskset_rocket_chat import TasksetRocketChat
from loadtests.loadtests.taskset_status_service import TasksetStatusService
from loadtests.loadtests.user import SchulcloudUser
from loadtests.loadtests.user_type import UserType

if Config.WEIGHT_PUPIL:
    class PupilUser(SchulcloudUser):

        type = UserType.PUPIL
        credentials = Config.LOGIN_PUPIL
        weight = Config.WEIGHT_PUPIL
        tasks = {
            TasksetBBB: 1,
            TasksetSchulCloud: 3,
            TasksetDoc: 1,
            TasksetRocketChat: 1
        }

if Config.WEIGHT_ADMIN:
    class AdminUser(SchulcloudUser):

        type = UserType.ADMIN
        credentials = Config.LOGIN_ADMIN
        weight = Config.WEIGHT_ADMIN
        tasks = {
            TasksetBBB: 1,
            TasksetSchulCloud: 3,
            TasksetDoc: 1,
            TasksetRocketChat: 1
        }

if Config.WEIGHT_TEACHER:
    class TeacherUser(SchulcloudUser):

        type = UserType.TEACHER
        credentials = Config.LOGIN_TEACHER
        weight = Config.WEIGHT_TEACHER
        tasks = {
            TasksetBBB: 1,
            TasksetSchulCloud: 3,
            TasksetDoc: 1,
            TasksetRocketChat: 1
        }

if Config.WEIGHT_ANONYMOUS:
    class AnonymousUser(SchulcloudUser):

        type = UserType.ANONYMOUS
        credentials = Config.LOGIN_ANONYMOUS
        weight = Config.WEIGHT_ANONYMOUS
        tasks = {
            TasksetStatusService: 1,
        }

if Config.WEIGHT_ACTUAL_ANONYMOUS:
    class ActualAnonymousUser(SchulcloudUser):

        type = UserType.ACTUAL_ANONYMOUS
        weight = Config.WEIGHT_ACTUAL_ANONYMOUS
        tasks = {
            TasksetAnonymous: 1
        }

        # override login / logout
        def on_start(self):
            pass

        def on_stop(self):
            pass

if Config.WEIGHT_EXTERNAL_PUPIL:
    class ExternalPupilUser(SchulcloudUser):

        type = UserType.EXTERNAL_PUPIL
        credentials = Config.LOGIN_EXTERN_PUPIL
        weight = Config.WEIGHT_EXTERNAL_PUPIL
        tasks = {
            TasksetBBB: 0,
            TasksetSchulCloud: 0,
            TasksetDoc: 0,
            TasksetRocketChat: 0,
            TasksetExternalLogin: 1
        }

        # override login / logout
        def on_start(self):
            print("User instance (%r) executes on_start " % self)
            pass

        def on_stop(self):
            print("User instance (%r) executes on_stop " % self)
            pass

# list all user classes for functional tests with weight greater 0
#user_classes: List[Type[SchulcloudUser]] = [users for users in [AdminUser, TeacherUser, PupilUser, AnonymousUser, ActualAnonymousUser, ExternalPupilUser] if users.weight > 0]
