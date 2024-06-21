from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileEditForm, ChangePasswordForm
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash


# Create your views here.
class RedirectAuthenticatedUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(RedirectAuthenticatedUserMixin, FormView):
    template_name = "user/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("user:login")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        user = form.save()

        messages.success(
            self.request,
            f"Account created successfully for {user.username}! You can now log in.",
        )
        return super().form_valid(form)


class CustomLoginView(RedirectAuthenticatedUserMixin, View):
    template_name = 'user/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}! You have successfully logged in.')
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        # If form is invalid or authentication fails, render login form with errors
        return render(request, self.template_name, {'form': form})


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect(reverse('user:login'))
    
    

class CustomForgotPassword(View):
    template_name = 'user/forgot_password.html'
    form_class = ForgotPasswordForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            
            if user is not None:
                current_site = get_current_site(request)
                mail_subject = 'Reset Your Password'
                message = render_to_string('user/reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.content_subtype = 'html'
                send_email.send()
                
                context = {
                    'email_sent': True,
                    'email': email,
                }
                return render(request, self.template_name, context)
            else:
                messages.error(request, 'Account does not exist.')
                return redirect('user:forgot-password')
        else:
            return render(request, self.template_name, {'form': form})
        
class ResetPasswordView(View):
    template_name = "user/reset_password.html"
    form_class = ResetPasswordForm
    
    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None
    
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        
        if user is not None and default_token_generator.check_token(user, token):
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('user:login')
    
    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        
        if user is not None and default_token_generator.check_token(user, token):
            form = self.form_class(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']

                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password reset successful. Please login with your new password.')
                    return redirect('user:login')
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('user:login')
        

class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = 'user/profile-edit.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('user:profile')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user  # Pass current user instance to form
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['username']
        user.save()

        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return self.render_to_response(self.get_context_data(form=form))


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'user/change-password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('user:profile-edit')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)