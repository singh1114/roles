from tweets.constants import TweetStatusConstants


def get_tweet_status_choices():
    return [
        ('INITIATED_CREATE', TweetStatusConstants.INITIATED_CREATE.value),
        ('APPROVED', TweetStatusConstants.APPROVED.value),
        ('DELETED', TweetStatusConstants.DELETED.value),
        ('INITIATED_DELETE', TweetStatusConstants.INITIATED_DELETE.value),
        ('INITIATED_UPDATE', TweetStatusConstants.INITIATED_UPDATE.value)
    ]
