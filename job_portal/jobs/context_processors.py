from .models import Job, JobPortalProfile


def job_context_processor(request):
    if request.user.is_authenticated:
        try:
            profile = JobPortalProfile.objects.get(user=request.user)
            jobs = Job.objects.exclude(user=profile)
            jobs_count = jobs.count()
        except JobPortalProfile.DoesNotExist:
            jobs = None
            jobs_count = 0
    else:
        jobs = None
        jobs_count = 0
    
    return {
        'jobs_notification': jobs,
        'jobs_notification_count': jobs_count,
    }
