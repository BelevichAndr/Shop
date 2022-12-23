from django.urls import path

from users.views import (EmailVerificationView, UserLoginView, UserLogoutView,
                         UserRegistrationView, profile)

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("profile/", profile, name="profile"),
    path("verify/<str:email>/<uuid:code>/", EmailVerificationView.as_view(), name="email_verification"),
]
