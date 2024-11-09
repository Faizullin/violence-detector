from dj_rest_auth.views import (LogoutView,
                                PasswordResetConfirmView, UserDetailsView)
from django.urls import path

from .views import LoginView, RegisterView, VerifyEmailView, TokenRefreshView, PasswordResetView

app_name = 'accounts'

urlpatterns = [
    path('api/v1/auth/register/', RegisterView.as_view(), name='rest_register'),
    path('api/v1/auth/login/token/', LoginView.as_view(), name='rest_login'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('api/v1/auth/verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    # path('api/v1/auth/account-confirm-email/',
    #      VerifyEmailView.as_view(), name='rest_resend_email'),
    # re_path(r'^api/v1/auth/account-confirm-email/(?P<key>[-:\w]+)/$',
    #         VerifyEmailView.as_view(), name='account_confirm_email'),
    path('api/v1/auth/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('api/v1/auth/password/reset/confirm/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/v1/auth/me/', UserDetailsView.as_view(), name='rest_user_details'),
]
