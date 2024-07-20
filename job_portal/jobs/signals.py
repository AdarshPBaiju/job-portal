from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job, JobApplication, Notification, NotificationList, JobPortalProfile


def create_notification(subject, content, job=None, job_application=None):
    notification, created = Notification.objects.get_or_create(
        job=job,
        job_application=job_application,
        defaults={
            'subject': subject,
            'content': content
        }
    )
    return notification, created

class JobSignals:
    @staticmethod
    @receiver(post_save, sender=Job)
    def create_job_notifications(sender, instance, created, **kwargs):
        if created:
            subject = f"New application received for {instance.job.job_title}"
            content = f"A new application has been received for the position of {instance.job.job_title} in {instance.job.location}."
            notification, _ = create_notification(subject, content, job_application=instance)
            
            try:
                employee = JobPortalProfile.objects.get(job=instance.job, job_profile='Employee')
                NotificationList.objects.get_or_create(
                    user=employee,
                    notification=notification
                )
            except JobPortalProfile.DoesNotExist:
                pass

class ApplicationSignals:
    @staticmethod
    @receiver(post_save, sender=JobApplication)
    def create_application_notifications(sender, instance, created, **kwargs):
        if created:
            subject = f"New application received for {instance.job.job_title}"
            content = f"A new application has been received for the position of {instance.job.job_title} in {instance.job.location}."
            notification, _ = create_notification(subject, content, job_application=instance)
            
            try:
                employee = JobPortalProfile.objects.get(job=instance.job, job_profile='Employee')
                NotificationList.objects.get_or_create(
                    user=employee,
                    notification=notification
                )
            except JobPortalProfile.DoesNotExist:
                pass


class ApplicationStatusChangeSignals:
    @staticmethod
    @receiver(post_save, sender=JobApplication)
    def update_application_status_notifications(sender, instance, created, **kwargs):
        if not created and instance.status in ['Selected', 'Rejected']:
            subject = f"Application status changed for {instance.job.job_title}"
            content = f"The application status for {instance.job.job_title} in {instance.job.location} has been changed to {instance.status}."
            
            notification = Notification.objects.create(
                job=None,
                job_application=instance,
                subject=subject,
                content=content
            )
            
            # Assign this notification to the job seeker (applicant) who applied for the job
            try:
                job_seeker = instance.applicant
                NotificationList.objects.create(
                    user=job_seeker,
                    notification=notification
                )
            except JobPortalProfile.DoesNotExist:
                pass