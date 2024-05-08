from django.urls import path, re_path
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, LogoutView
from .views import CustomRegisterView, CustomLoginView, CustomConfirmEmailView, IsEmailConfirmed


urlpatterns = [
    path('api/registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('api/login/', CustomLoginView.as_view(), name='login'), 
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('api/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api/check-email-verify/', IsEmailConfirmed.as_view(), name='check-email-verify'),
    re_path(r'^api/account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    re_path(
        r'^api/registration/account-confirm-email/(?P<key>[-:\w]+)/$', CustomConfirmEmailView.as_view(),
        name='account_confirm_email',
    ),
    path('api/resend-account-confirm-email', ResendEmailVerificationView.as_view(), name='resend-email-confirm'),
    path('api/password-reset/', PasswordResetView.as_view(), name='reset_password'),
    path('api/password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
