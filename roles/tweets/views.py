from django.contrib.auth.models import User

from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.constants import LogTypeConstants, LogActionConstants
from base.models import ActionLogModel
from base.views import AbstractAPIView

from tweets.constants import TweetStatusConstants
from tweets.models import Tweet
from tweets.permissions import IsNormalUser, IsAdminUser, IsSuperAdminUser


class TweetView(AbstractAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsNormalUser)

    def get(self, request, *args, **kwargs):
        self.log_type = LogTypeConstants.ACCESS
        self.log_action = LogActionConstants.GET_TWEETS
        tweets = Tweet.objects.filter(
            user=request.user,
            status=TweetStatusConstants.APPROVED.value).order_by('-created_at')
        return Response([{
            'id': tweet.id,
            'text': tweet.text,
            'created_at': tweet.created_at
        } for tweet in tweets],
            status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.log_type = LogTypeConstants.ACTION
        self.log_action = LogActionConstants.TWEET
        text = request.data.get('text')
        try:
            tweet = Tweet.objects.create(text=text, user=request.user)
            self.log_object = tweet
        except Exception as e:
            # log the exception. Use a logger class later.
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Added successfully'},
                        status=status.HTTP_200_OK)

    def delete(self, request, id, *args, **kwargs):
        self.log_type = LogTypeConstants.AUDIT
        self.log_action = LogActionConstants.TWEET
        try:
            tweet = Tweet.objects.get(id=id, user=request.user)
            tweet.status = TweetStatusConstants.DELETED.value
            tweet.save()
            self.log_object = tweet
        except Exception as e:
            # log the exception.
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Deleted Successfully'},
                        status=status.HTTP_200_OK)


class AdminTweetView(AbstractAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, user_id, *args, **kwargs):
        self.log_type = LogTypeConstants.ACCESS
        self.log_action = LogActionConstants.GET_TWEETS
        tweets = Tweet.objects.filter(
            user__id=user_id).order_by('-created_at')
        return Response([{
            'id': tweet.id,
            'text': tweet.text,
            'created_at': tweet.created_at,
            'status': TweetStatusConstants(tweet.status).name,
            'updated_text': tweet.updated_text
        } for tweet in tweets],
            status=status.HTTP_200_OK)

    def post(self, request, user_id, *args, **kwargs):
        self.log_type = LogTypeConstants.ACTION
        self.log_action = LogActionConstants.TWEET
        text = request.data.get('text')
        try:
            user = User.objects.get(id=user_id)
            tweet = Tweet.objects.create(text=text, user=user,
                                         status=TweetStatusConstants.INITIATED_CREATE.value)
            self.log_object = tweet
        except Exception as e:
            # log the exception. Use a logger class later.
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Added successfully'},
                        status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        self.log_type = LogTypeConstants.ACTION
        self.log_action = LogActionConstants.REQUESTED_CHANGE
        text = request.data.get('text')
        try:
            tweet = Tweet.objects.get(id=id)
            tweet.updated_text = text
            tweet.status = TweetStatusConstants.INITIATED_UPDATE.value
            tweet.save()
            self.log_object = tweet
        except Exception as e:
            # log the exception. Use a logger class later.
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Updated successfully'},
                        status=status.HTTP_200_OK)

    def delete(self, request, id, *args, **kwargs):
        self.log_type = LogTypeConstants.AUDIT
        self.log_action = LogActionConstants.DELETE
        try:
            tweet = Tweet.objects.get(id=id)
            tweet.status = TweetStatusConstants.INITIATED_DELETE.value
            tweet.save()
            self.log_object = tweet
        except Exception as e:
            # log the exception.
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Deleted Successfully'},
                        status=status.HTTP_200_OK)


class ApproveChange(AbstractAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    def get(self, request, id=None):
        if not id:
            tweets = Tweet.objects.exclude(status__in=(
                TweetStatusConstants.APPROVED.value, TweetStatusConstants.DELETED.value)) \
                .order_by('-created_at')
            return Response([{
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'status': TweetStatusConstants(tweet.status).name,
                'updated_text': tweet.updated_text
            } for tweet in tweets], status=status.HTTP_200_OK)
        tweet = Tweet.objects.get(id=id)
        if tweet.status == TweetStatusConstants.INITIATED_CREATE.value:
            tweet.status = TweetStatusConstants.APPROVED.value
            tweet.save()
            self.log_type = LogTypeConstants.AUDIT
            self.log_action = LogActionConstants.TWEET
            self.log_object = tweet
        elif tweet.status == TweetStatusConstants.INITIATED_DELETE.value:
            tweet.status = TweetStatusConstants.DELETED.value
            tweet.save()
            self.log_type = LogTypeConstants.AUDIT
            self.log_action = LogActionConstants.DELETE
            self.log_object = tweet
        elif tweet.status == TweetStatusConstants.INITIATED_UPDATE.value:
            tweet.status = TweetStatusConstants.INITIATED_UPDATE.value
            tweet.text = tweet.updated_text
            tweet.save()
            self.log_type = LogTypeConstants.AUDIT
            self.log_action = LogActionConstants.REQUESTED_CHANGE
            self.log_object = tweet
        return Response({'message': 'Request Approved'})


class ReadAuditLogs(AbstractAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    def get(self, request, *args, **kwargs):
        self.log_type = LogTypeConstants.AUDIT
        self.log_action = LogActionConstants.READ_LOGS
        action_logs = ActionLogModel.objects.all().order_by('-created_at')
        return Response([{
            'id': action_log.id,
            'user': action_log.user.username if action_log.user else None,
            'log_type': LogTypeConstants(action_log.log_type).name,
            'action': LogActionConstants(action_log.action).name,
            # Forcing string representation.
            'content_object': str(action_log.content_object),
            'created_at': action_log.created_at
        } for action_log in action_logs], status=status.HTTP_200_OK)

