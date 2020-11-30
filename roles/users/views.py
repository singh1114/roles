from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from base.constants import LogTypeConstants, LogActionConstants
from base.views import AbstractAPIView


class SignupView(AbstractAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        self.log_type = LogTypeConstants.ACCESS
        self.log_action = LogActionConstants.GET_TWEETS
        user = User.objects.create_user(
            username=username, password=password)
        group = Group.objects.get(name='USER')
        user.groups.add(group)
        return Response({
            'id': user.id,
            'username': user.username,
            'access': str(RefreshToken.for_user(user).access_token),
            'group': group.name
        },
            status=status.HTTP_200_OK)
