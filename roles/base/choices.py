from base.constants import LogTypeConstants, LogActionConstants


def get_log_type_choices():
    return [
        ('ACCESS', LogTypeConstants.ACCESS.value),
        ('AUDIT', LogTypeConstants.AUDIT.value),
        ('ACTION', LogTypeConstants.ACTION.value)
    ]


def get_log_action_choices():
    return [
        ('TWEET', LogActionConstants.TWEET.value),
        ('LOGIN', LogActionConstants.LOGIN.value),
        ('DELETE', LogActionConstants.DELETE.value),
        ('REQUESTED_CHANGE', LogActionConstants.REQUESTED_CHANGE.value),
        ('APPROVED', LogActionConstants.APPROVED.value),
        ('GET_TWEETS', LogActionConstants.GET_TWEETS.value),
        ('SIGN_UP', LogActionConstants.SIGN_UP.value),
        ('READ_LOGS', LogActionConstants.READ_LOGS.value)
    ]

