from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'admin_panel/index.html'

class LoginView(TemplateView):
    template_name = 'admin_panel/login.html'

class ProfileView(TemplateView):
    template_name = 'admin_panel/profile.html'

class ProfileEditView(TemplateView):
    template_name = 'admin_panel/edit-profile.html'

class UsersListView(TemplateView):
    template_name = 'admin_panel/userslist.html'

class UserUpdateView(TemplateView):
    template_name = 'admin_panel/edit-user.html'

class UserCreateView(TemplateView):
    template_name = 'admin_panel/add-user.html'

class UserDetailView(TemplateView):
    template_name = 'admin_panel/User-detail.html'

class CompaniesListView(TemplateView):
    template_name = 'admin_panel/companieslist.html'

class CompanyAddView(TemplateView):
    template_name = 'admin_panel/add-company.html'

class CompanyUpdateView(TemplateView):
    template_name = 'admin_panel/companieslist.html'

class CompanyDetailView(TemplateView):
    template_name = 'admin_panel/company-detail.html'

class CompanyDetailInterviewListView(TemplateView):
    template_name = 'admin_panel/company-detail-interview.html'

class CompanyDetailApplicantListView(TemplateView):
    template_name = 'admin_panel/company-detail-applicant-list.html'

class JobListView(TemplateView):
    template_name = 'admin_panel/job-list.html'

class JobDetailView(TemplateView):
    template_name = 'admin_panel/job-detail.html'

class JobDetailInterviewListView(TemplateView):
    template_name = 'admin_panel/job-detail-schedule.html'

class JobCreateView(TemplateView):
    template_name = 'admin_panel/add-job.html'

class JobUpdateView(TemplateView):
    template_name = 'admin_panel/job-edit.html'