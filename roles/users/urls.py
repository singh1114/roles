from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from users.views import SignupView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', SignupView.as_view(), name='sign_up_user')
]
