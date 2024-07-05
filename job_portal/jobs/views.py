from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, CreateView
from .forms import EmployeeForm, JobSeekerForm
from .models import Job, JobPortalProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class JobListView(LoginRequiredMixin, View):
    template_name = 'jobs/job.html'
    
    def get(self, request, *args, **kwargs):
        job_list = Job.objects.exclude(user=request.user.jobportalprofile).order_by('-created_at')
        context = {
            'jobs': job_list,
        }
        return render(request, self.template_name, context)
    
    
# Job Profile Select View
class JobProfileSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/select_jobprofile.html'
    
    def dispatch(self, request, *args, **kwargs):
        if JobPortalProfile.objects.filter(user=request.user).exists():
            return redirect('user:profile_view')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        job_type = self.request.GET.get('type', None)
        
        if job_type == 'employer':
            return redirect(reverse_lazy('job:create_employee_profile'))
        elif job_type == 'jobseeker':
            return redirect(reverse_lazy('job:create_job_seeker_profile'))
        else:
            return super().get(request, *args, **kwargs)


# job Seeker create view
class JobSeekerProfileCreateView(CreateView):
    model = JobPortalProfile
    form_class = JobSeekerForm
    template_name = "jobs/job_seeker_create.html"
    success_url = reverse_lazy('user:profile_view')
    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.job_profile = 'Job Seeker'
        profile.company = None
        profile.location = None
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)


class EmployeeProfileCreateView(LoginRequiredMixin, CreateView):
    model = JobPortalProfile
    form_class = EmployeeForm
    template_name = "jobs/employee_create.html"
    success_url = reverse_lazy('user:profile_view')

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.job_profile = 'Employee'
        profile.expertise_level = None
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

