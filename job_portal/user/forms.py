from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from django.core.validators import MinLengthValidator
from django.forms import EmailInput, Select, CheckboxInput,CharField, SelectMultiple
from django.forms import TextInput, PasswordInput, Textarea, FileInput, DateInput
from .validators import validate_video_file

# user registration
class UserRegistrationForm(forms.ModelForm):
    confirm_password = CharField(
        max_length = 25,
        min_length = 8,
        required = True,
        validators = [
            MinLengthValidator(8, 'The password is too short.')
        ],
        widget = PasswordInput({
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'phone',
        ]
        
        widgets = {
            'username': TextInput({
                'class': 'form-control',
                'placeholder':'Enter Username'
            }),

            'email': EmailInput({
                'class': 'form-control'
            }),
            
            'first_name': TextInput({
                'class': 'form-control',
                'autocomplete': 'first_name'
            }),

            'last_name': TextInput({
                'class': 'form-control'
            }),
            
            'password': PasswordInput({
                'class': 'form-control'
            }),

            'phone': TextInput({
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please enter the same password in both fields.")

        return cleaned_data
    

# Profile Add
class ProfileAddForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'profile_photo',
            'dob',
            'short_bio',
            'job_title',
            'qualification',
            'hobby',
            'interest',
            'smoking_habit',
            'drinking_habit',
            'gender',
            'country',
            'open_to_hiring',
            'short_reel'
        ]

        widgets = {
            'dob': DateInput({
                'class': 'form-control',
                'type': 'date'
            }),

            'short_bio': Textarea({
                'class': 'form-control',
                'rows': '3'
            }),

            'job_title': TextInput({
                'class': 'form-control'
            }),

            'qualification': Select({
                'class': 'form-control'
            }),

            'hobby': SelectMultiple({
                'class': 'form-control'
            }),

            'interest': SelectMultiple({
                'class': 'form-control'
            }),

            'smoking_habit': Select({
                'class': 'form-control'
            }),

            'drinking_habit': Select({
                'class': 'form-control'
            }),

            'gender': Select({
                'class': 'form-control'
            }),

            'country': Select({
                'class': 'form-control'
            }),

            'open_to_hiring': CheckboxInput({
                'class': 'form-check-input'
            }),

            'profile_photo': FileInput({
                'class': 'form-control'
            }),

            'short_reel': FileInput({
                'class': 'form-control',
                'accept': 'video/mp4, video/avi, video/mkv, video/mov, video/wmv'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'open_to_hiring':
                field.required = True


            
    def clean_short_reel(self):
        short_reel = self.cleaned_data.get('short_reel', False)
        if not short_reel:
            raise forms.ValidationError("No file chosen!")

        validate_video_file(short_reel)
        return short_reel


# user login
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        max_length=254
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    

# Forgot Password Email Form 
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    

# Reset Password Form
class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        label='Confirm Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data


# Profile Update
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'profile_photo',
            'dob',
            'short_bio',
            'job_title',
            'qualification',
            'hobby',
            'interest',
            'smoking_habit',
            'drinking_habit',
            'gender',
            'country',
            'open_to_hiring',
            'short_reel'
        ]

        widgets = {
            'username': TextInput({
                'class': 'form-control'
            }),

            'email': EmailInput({
                'class': 'form-control'
            }),
            
            'first_name': TextInput({
                'class': 'form-control'
            }),

            'last_name': TextInput({
                'class': 'form-control'
            }),

            'phone': TextInput({
                'class': 'form-control'
            }),

            'dob': DateInput({
                'class': 'form-control',
                'type': 'date'
            }),

            'short_bio': Textarea({
                'class': 'form-control',
                'rows': '3'
            }),

            'job_title': TextInput({
                'class': 'form-control'
            }),

            'qualification': Select({
                'class': 'form-control'
            }),

            'hobby': SelectMultiple({
                'class': 'form-control'
            }),

            'interest': SelectMultiple({
                'class': 'form-control'
            }),

            'smoking_habit': Select({
                'class': 'form-control'
            }),

            'drinking_habit': Select({
                'class': 'form-control'
            }),

            'gender': Select({
                'class': 'form-control'
            }),

            'country': Select({
                'class': 'form-control'
            }),

            'open_to_hiring': CheckboxInput({
                'class': 'form-check-input'
            }),

            'profile_photo': FileInput({
                'class': 'form-control'
            }),

            'short_reel': FileInput({
                'class': 'form-control',
                'accept': 'video/mp4, video/avi, video/mkv, video/mov, video/wmv'
            })
        }
    def clean_short_reel(self):
        short_reel = self.cleaned_data.get('short_reel', False)
        if not short_reel:
            raise forms.ValidationError("No file chosen!")

        validate_video_file(short_reel)
        return short_reel
    
    
# Change Password
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter old password'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'})
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']


# Address
class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'name': TextInput({
                'class': 'form-control',
                'autocomplete': 'name'
            }),

            'address_line_1': TextInput({
                'class': 'form-control',
                'autocomplete': 'address_line_1'
            }),

            'address_line_2': TextInput({
                'class': 'form-control'
            }),

            'address_line_3': TextInput({
                'class': 'form-control'
            }),

            'city': TextInput({
                'class': 'form-control'
            }),

            'state': TextInput({
                'class': 'form-control'
            }),

            'pincode': TextInput({
                'class': 'form-control'
            }),

            'country': Select({
                'class': 'form-control'
            }),

            'phone': TextInput({
                'class': 'form-control'
            }),

            'is_default': CheckboxInput(),
        }


# Experience
class ExperienceUpsertForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['user']
        widgets = {
            'title': TextInput({
                'class': 'form-control',
                'autocomplete': 'title'
            }),

            'company': TextInput({
                'class': 'form-control',
                'autocomplete': 'company'
            }),

            'location': TextInput({
                'class': 'form-control'
            }),

            'description': Textarea({
                'class': 'form-control',
                'rows':'4'
            }),

            'start_date': DateInput({
                'class': 'form-control',
                'type': 'date'
            }),

            'end_date': DateInput({
                'class': 'form-control',
                'required':False,
                'type': 'date'
            }),
        }


# Education
class EducationUpsertForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['user']
        widgets = {
            'institution': TextInput({
                'class' : 'form-control',
            }),

            'degree': Select({
                'class': 'form-control',
            }),

            'field_of_study': TextInput({
                'class': 'form-control',
            }),

            'start_date': DateInput({
                'class': 'form-control',
                'type': 'date',
            }),

            'end_date': DateInput({
                'class': 'form-control',
                'required':False,
                'type': 'date'
            }),
        }    


# UserSkill
class UserSkillUpsertForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        exclude = ['user']
        widgets = {
            'skill': Select({
                'class' : 'form-control',
                'autocomplete': 'skill',
                'placeholder' : 'Skill'
            }),

            'level': Select({
                'class': 'form-control',
                'autocomplete': 'level',
                'placeholder' : 'level'
            }),
        }    