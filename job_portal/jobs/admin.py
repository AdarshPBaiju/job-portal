from django.contrib import admin

from .models import Company, Industry, JobPortalProfile, JobTitle

# Register your models here.
admin.site.register(JobTitle)
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(JobPortalProfile)