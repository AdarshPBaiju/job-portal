from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, CreateView
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import EmployeeForm, JobApplicationForm, JobSeekerForm
from .models import Job, JobApplication, JobPortalProfile, NotificationList
from job_portal.mixin import JobPortalProfileRequiredMixin


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
class JobSeekerProfileUpsertView(LoginRequiredMixin, View):
    template_name = "jobs/job_seeker_create.html"
    success_url = reverse_lazy('user:job_profile')

    def get(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = JobSeekerForm(instance=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = JobSeekerForm(request.POST, instance=profile)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_profile(self, request):
        try:
            return JobPortalProfile.objects.get(user=request.user)
        except JobPortalProfile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.job_profile = 'Job Seeker'
        profile.company = None
        profile.location = None
        profile.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class EmployeeProfileUpsertView(LoginRequiredMixin, View):
    template_name = "jobs/employee_create.html"
    success_url = reverse_lazy('user:job_profile')

    def get(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = EmployeeForm(instance=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = EmployeeForm(request.POST, instance=profile)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_profile(self, request):
        try:
            return JobPortalProfile.objects.get(user=request.user)
        except JobPortalProfile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.job_profile = 'Employee'
        profile.expertise_level = None
        profile.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


# Job List View
class JobListView(LoginRequiredMixin, JobPortalProfileRequiredMixin, View):
    template_name = 'jobs/job.html'
    paginate_by = 1
    
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q', '')
        
        if search_query:
            job_list = Job.objects.filter(
                job_title__title__icontains=search_query
            ).exclude(
                user=request.user.jobportalprofile
            ).order_by('-created_at')
        else:
            job_list = Job.objects.filter(
                job_title__title__icontains=request.user.jobportalprofile.title
            ).exclude(
                user=request.user.jobportalprofile
            ).order_by('-created_at')
        
        paginator = Paginator(job_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        applied_job_ids = JobApplication.objects.filter(applicant=request.user.jobportalprofile).values_list('job_id', flat=True)

        context = {
            'jobs': page_obj,
            'search_query': search_query,
            'applied_job_ids': applied_job_ids,
        }
        return render(request, self.template_name, context)
    

# Job Detail View
class JobDetailView(LoginRequiredMixin, JobPortalProfileRequiredMixin, DetailView):
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
class JobApplicationCreateView(LoginRequiredMixin, JobPortalProfileRequiredMixin, CreateView):
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
        messages.success(self.request, f'You have successfully applied for the job: {job.job_title.title}')
        return super().form_valid(form)


class JobApplicationSuccessView(LoginRequiredMixin, JobPortalProfileRequiredMixin, DetailView):
    model = JobApplication
    template_name = 'jobs/job_application_success.html'
    context_object_name = 'application'

    def get_object(self):
        try:
            return JobApplication.objects.get(pk=self.kwargs['pk'], applicant=self.request.user.jobportalprofile)
        except self.model.DoesNotExist:
            raise Http404('Job application not found.')


# Notification
class GetNotificationsView(View):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user.jobportalprofile
            notifications = NotificationList.objects.filter(user=user).select_related('notification')

            data = []
            for notification in notifications:
                notification_data = {
                    'id': notification.id,
                    'subject': notification.notification.subject,
                    'content': notification.notification.content,
                    'created': notification.notification.created,
                    'is_read': notification.is_read,
                    'url': self.get_notification_url(notification, request)
                }
                data.append(notification_data)

            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get_notification_url(self, notification, request):
        if notification.notification.job:
            return reverse_lazy('job:job-detail', args=[notification.notification.job.id])
        elif notification.notification.job_application:
            # If the notification is related to a job application
            if request.user.jobportalprofile.job_profile == 'Employee':
                # Return the URL for the employee's application list
                return reverse_lazy('user:application-list', args=[notification.notification.job_application.job.id])
            else:
                # Return the URL for the applicant's application list
                return reverse_lazy('user:job_applications_for_applicants')
        else:
            # Handle case where no URL is applicable
            return reverse_lazy('core:home')
    
class NotificationDataView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            # Get unread notifications count
            user_profile = request.user.jobportalprofile
            unread_count = NotificationList.objects.filter(user=user_profile, is_read=False).count()

            # Mark all unread notifications as read
            NotificationList.objects.filter(user=user_profile, is_read=False).update(is_read=True)

            return JsonResponse({'unread_count': unread_count})
        except JobPortalProfile.DoesNotExist:
            return JsonResponse({'error': 'Profile not found'}, status=404)