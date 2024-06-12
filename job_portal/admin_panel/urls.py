from django.urls import path
from .views import *


app_name = 'admin_panel'

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("users/", UsersListView.as_view(), name="userslist"),
    path("users/Detail/", UserDetailView.as_view(), name="userdetail"),
    path("companies/", CompaniesListView.as_view(), name="companylist"),
    path("companies/detail/", CompaniesDetailView.as_view(), name="companydetail"),
]
