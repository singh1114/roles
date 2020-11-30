from tweets.constants import TweetStatusConstants


def get_tweet_status_choices():
    return [
        ('INITIATED_CREATE', TweetStatusConstants.INITIATED_CREATE),
        ('APPROVED', TweetStatusConstants.APPROVED),
        ('DELETED', TweetStatusConstants.DELETED),
        ('INITIATED_DELETE', TweetStatusConstants.INITIATED_DELETE),
        ('INITIATED_UPDATE', TweetStatusConstants.INITIATED_UPDATE)
    ]
