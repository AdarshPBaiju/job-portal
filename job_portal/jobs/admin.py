from django.contrib import admin

from .models import Company, Industry, JobPortalProfile, JobTitle,Job

# Register your models here.
admin.site.register(JobTitle)
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(JobPortalProfile)
admin.site.register(Job)