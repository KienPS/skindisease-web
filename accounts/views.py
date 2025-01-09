from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import UserRegisterForm


class RegisterView(CreateView, SuccessMessageMixin):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')
    form_class = UserRegisterForm
    success_message = 'User created successfully'


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('accounts:profile')
    fields = ['first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        return self.request.user
