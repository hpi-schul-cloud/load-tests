import functions
import loginout
import locustfile

from locust.user.task import TaskSet, tag, task

class rocketChatTaskSet(TaskSet):

    # Lists which contain all the doc/courses/teams ID's beeing created from the loadtest. 
    # All three lists are necessary for a clean log-out process in 'loginout'.
    createdDocuments = []
    createdCourses = []
    createdTeams = []

    def on_start(self):
        loginout.login(self)

    def on_stop(self):
        loginout.logout(self)

    @tag('rocketChat')
    @task
    def createTeamWithRocketChat(self):
        '''
        This task creates a new team and enables the team-messenger (settings). Afterwards, it opens the team-messenger and 
        posts some chat messanges. At the end, the created team will be deleted. 
        Note: only teacher or admins can create a new team.
        '''
        # Create team
        # Enable team messenger
        # Post messages
        # Delete team -> functions.deleteTeam(self, teamId)

        if isinstance(self._user, locustfile.PupilUser) is False:
            teamId = functions.newTeam(self)
            functions.enableTeamMessenger(self)#, teamId)
        

        