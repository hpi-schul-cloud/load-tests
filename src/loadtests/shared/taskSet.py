

class User:
    """
    Neutral user
    """
    
    def __init__(self, credentials) -> None:
        pass


class TaskSet:
    """
    Neutral task set
    """

    def __init__(self, user: User) -> None:
        self.user = user

    def login(self):
        pass
