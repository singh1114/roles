from django.contrib.auth.models import AnonymousUser

from rest_framework.views import APIView

from base.models import ActionLogModel


class AbstractAPIView(APIView):
    log_type = None
    log_action = None
    log_object = None

    def finalize_response(self, request, response, *args, **kwargs):
        if self.log_type and self.log_action:
            user = request.user
            if isinstance(user, AnonymousUser):
                user = None
            ActionLogModel.objects.create(
                user=user, log_type=self.log_type,
                action=self.log_action, content_object=self.log_object)
        return super().finalize_response(request, response, args, kwargs)
