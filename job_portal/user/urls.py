from django.urls import path
from .views import *


app_name = "user"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("forgot-password/", CustomForgotPassword.as_view(), name="forgot-password"),
    path("reset-password/validate/<uidb64>/<token>/", ResetPasswordView.as_view(), name="reset_password_validate"),
]