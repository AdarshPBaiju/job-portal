from django.urls import path
from .views import *


app_name = 'admin_panel'

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("users/", UsersListView.as_view(), name="userslist"),
    path("companies/", CompaniesListView.as_view(), name="companylist"),
]
