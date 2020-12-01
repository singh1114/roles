from enum import Enum


class TweetStatusConstants(Enum):
    INITIATED_CREATE = 1
    APPROVED = 2
    DELETED = 3
    INITIATED_DELETE = 4
    INITIATED_UPDATE = 5
