from django.views.generic import TemplateView
from .forms import UserRegistrationForm
from django.views.generic import FormView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect


# Create your views here.

class RedirectAuthenticatedUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)



class Login(RedirectAuthenticatedUserMixin, LoginView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('core:home')

class Register(RedirectAuthenticatedUserMixin, FormView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/register.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class Logout(LogoutView):
    next_page = 'user:login'