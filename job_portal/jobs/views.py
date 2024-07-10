from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, CreateView, ListView
from .forms import EmployeeForm, JobApplicationForm, JobSeekerForm
from .models import Job, JobApplication, JobPortalProfile
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.    
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
class JobSeekerProfileCreateView(LoginRequiredMixin ,CreateView):
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


# Job List View
class JobListView(LoginRequiredMixin, View):
    template_name = 'jobs/job.html'
    paginate_by = 2
    
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q', '')
        
        job_list = Job.objects.filter(
            job_title__title__icontains=search_query
        ).exclude(
            user=request.user.jobportalprofile
        ).order_by('-created_at')
        
        paginator = Paginator(job_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'jobs': page_obj,
            'search_query': search_query,
        }
        return render(request, self.template_name, context)
    

# Job Detail View
class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'jobs/job-detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        applicant = self.request.user.jobportalprofile
        context['already_applied'] = JobApplication.objects.filter(job=job, applicant=applicant).exists()
        return context
    
 
# Job Application   
class JobApplicationCreateView(LoginRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'jobs/job_apply.html'
    
    def get_success_url(self):
        return reverse_lazy('job:job_application_success', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        applicant = self.request.user.jobportalprofile

        if JobApplication.objects.filter(job=job, applicant=applicant).exists():
            messages.error(self.request, 'You have already applied for this job.')
            return redirect('job:job-detail', pk=job.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        initial['job'] = job
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        context['job'] = job
        return context

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        applicant = self.request.user.jobportalprofile
        form.instance.applicant = applicant
        form.instance.job = job
        return super().form_valid(form)


class JobApplicationSuccessView(DetailView):
    model = JobApplication
    template_name = 'jobs/job_application_success.html'
    context_object_name = 'application'

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs['pk'])


class JobApplicationListView(LoginRequiredMixin, View):
    template_name = 'jobs/job_applications.html'

    def get(self, request, *args, **kwargs):
        job_id = kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)

        if job.user != request.user.jobportalprofile:
            messages.error(request, "You do not have permission to view this job's applications.")
            return redirect('user:job-list')

        status_filter = request.GET.get('status', '')
        applications = JobApplication.objects.filter(job=job)
        
        if status_filter:
            applications = applications.filter(status=status_filter)

        context = {
            'applications': applications,
            'job': job,
            'selected_status': status_filter,
            'STATUS_CHOICES': JobApplication.STATUS,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        job_id = kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)

        if job.user != request.user.jobportalprofile:
            messages.error(request, "You do not have permission to modify this job's applications.")
            return redirect('user:job-list')

        action = request.POST.get('action')
        application_id = request.POST.get('application_id')
        application = get_object_or_404(JobApplication, id=application_id, job=job)

        if action == 'select':
            application.status = 'Selected'
        elif action == 'reject':
            application.status = 'Rejected'
        elif action == 'undo':
            application.status = 'Applied'

        application.save()
        messages.success(request, f"Application status updated to {application.status}.")
        return redirect('job:application-list', job_id=job_id)