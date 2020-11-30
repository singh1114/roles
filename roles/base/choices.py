from base.constants import LogTypeConstants, LogActionConstants


def get_log_type_choices():
    return [
        ('ACCESS', LogTypeConstants.ACCESS),
        ('AUDIT', LogTypeConstants.AUDIT),
        ('ACTION', LogTypeConstants.ACTION)
    ]


def get_log_action_choices():
    return [
        ('TWEET', LogActionConstants.TWEET),
        ('LOGIN', LogActionConstants.LOGIN),
        ('DELETE', LogActionConstants.DELETE),
        ('REQUESTED_CHANGE', LogActionConstants.REQUESTED_CHANGE),
        ('APPROVED', LogActionConstants.APPROVED),
        ('GET_TWEETS', LogActionConstants.GET_TWEETS),
        ('SIGN_UP', LogActionConstants.SIGN_UP),
        ('READ_LOGS', LogActionConstants.READ_LOGS)
    ]

