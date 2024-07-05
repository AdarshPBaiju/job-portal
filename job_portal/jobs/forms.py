from django import forms
from .models import Job, JobPortalProfile


class JobSeekerForm(forms.ModelForm):
    
    class Meta:
        model = JobPortalProfile
        fields = [
            'title',
            'expertise_level',
        ]
        
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control','required':True}),
            'expertise_level': forms.Select(attrs={'class': 'form-control','required':True})
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.job_profile = 'Job Seeker'
        instance.company = None
        instance.location = None
        if commit:
            instance.save()
        return instance


# Employee Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = JobPortalProfile
        fields = [
            'title',
            'company',
            'location',
            ]
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control', 'required':True}),
            'company': forms.Select(attrs={'class': 'form-control','required':True}),
            'location': forms.Select(attrs={'class': 'form-control', 'required':True}),
        }


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.job_profile = 'Employee'
        if commit:
            instance.save()
        return instance