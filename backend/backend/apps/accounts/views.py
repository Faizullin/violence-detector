from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView as _BaseRegisterView, VerifyEmailView as _BaseVerifyEmailView
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import LoginView as _BaseLoginView, PasswordResetView as _BasePasswordResetView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .serializers import UserProfileSerializer


class LoginView(_BaseLoginView):
    def login(self):
        self.user = self.serializer.validated_data['user']
        self.access_token, self.refresh_token = jwt_encode(self.user)


class RegisterView(_BaseRegisterView):
    pass


class VerifyEmailView(_BaseVerifyEmailView):
    pass


class TokenRefreshView(get_refresh_view()):
    pass


class PasswordResetView(_BasePasswordResetView):
    pass


class UserProfileView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
