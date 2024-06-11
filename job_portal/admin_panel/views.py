from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'admin_panel/index.html'

class UsersListView(TemplateView):
    template_name = 'admin_panel/userslist.html'

class CompaniesListView(TemplateView):
    template_name = 'admin_panel/companieslist.html'