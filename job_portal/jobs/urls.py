from django.urls import path
from .views import EmployeeProfileCreateView, JobListView, JobProfileSelectView, JobSeekerProfileCreateView, JobDetailView

app_name = 'jobs'

urlpatterns = [
    # Jobs
    path('', JobListView.as_view(), name='home'),
    path('<int:pk>', JobDetailView.as_view(), name='job-detail'),
    
    # JobProfile
    path('select-profile/', JobProfileSelectView.as_view(), name='select_profile'),
    path('create/job-seeker/', JobSeekerProfileCreateView.as_view(), name='create_job_seeker_profile'),
    path('create/employee/', EmployeeProfileCreateView.as_view(), name='create_employee_profile'),
]
