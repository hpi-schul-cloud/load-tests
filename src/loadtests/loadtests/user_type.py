
import enum


class UserType(enum.Enum):
    UNDEFINED = 0
    ADMIN = 1
    TEACHER = 2
    PUPIL = 3
    ANONYMOUS = 4
    ACTUAL_ANONYMOUS = 5
