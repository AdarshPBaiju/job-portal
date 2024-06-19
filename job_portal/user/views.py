from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
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
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! You have successfully logged in.')
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
        return render(request, self.template_name)


class CustomLogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect(reverse('user:login'))
    
    

class CustomForgotPassword(RedirectAuthenticatedUserMixin, View):
    template_name = 'user/forgot_password.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST.get('email')
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
                'token': default_token_generator.make_token(user)
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
        
class ResetPasswordView(RedirectAuthenticatedUserMixin, View):
    template_name = "user/reset_password.html"
    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None
    
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        
        if user is not None and default_token_generator.check_token(user, token):
            return render(request, self.template_name)
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('user:login')
    
    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        
        if user is not None and default_token_generator.check_token(user, token):
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful. Please login with your new password.')
                return redirect('user:login')
            else:
                messages.error(request, 'Passwords do not match. Please try again.')
                return render(request, self.template_name)
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('user:login')