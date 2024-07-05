from django.urls import path
from .views import EmployeeProfileCreateView, JobListView, JobProfileSelectView, JobSeekerProfileCreateView

app_name = 'jobs'

urlpatterns = [
    path('', JobListView.as_view(), name='home'),
    
    # JobProfile
    path('select-profile/', JobProfileSelectView.as_view(), name='select_profile'),
    path('create/job-seeker/', JobSeekerProfileCreateView.as_view(), name='create_job_seeker_profile'),
    path('create/employee/', EmployeeProfileCreateView.as_view(), name='create_employee_profile'),
]
