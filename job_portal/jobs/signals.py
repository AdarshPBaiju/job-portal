from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job, JobApplication, Notification, NotificationList, JobPortalProfile

class JobSignals:
    @staticmethod
    @receiver(post_save, sender=Job)
    def create_job_notifications(sender, instance, created, **kwargs):
        if created:
            notification, created = Notification.objects.get_or_create(
                job=instance,
                job_application=None,
                defaults={
                    'subject': f"New job posted: {instance.job_title}",
                    'content': f"A new job has been posted for the position of {instance.job_title} in {instance.location}."
                }
            )
            if created:
                # Assign this notification to all job seekers with the same job title
                job_seekers = JobPortalProfile.objects.filter(title=instance.job_title, job_profile='Job Seeker')
                for seeker in job_seekers:
                    NotificationList.objects.get_or_create(
                        user=seeker,
                        notification=notification
                    )