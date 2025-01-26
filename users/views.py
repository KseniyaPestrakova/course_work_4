from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.core.mail import send_mail
from django.contrib.auth import login

from config.settings import EMAIL_HOST_USER
from .forms import UserRegisterForm, CustomUserUpdateForm, UserManagerForm
from .models import CustomUser
import secrets


class RegisterView(FormView):
    model = CustomUser
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/confirm/{token}'
        send_mail(subject='Подтверждение регистрации в сервисе',
                  message=f'Добро пожаловать в наш сервис! Для подтверждения регистрации пройдите по ссылке ниже:\n'
                          f'{url}',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email])
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = 'customuser_detail.html'


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'register.html'
    success_url = reverse_lazy('mailing:home')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.pk:
            return CustomUser
        elif user.has_perm("blocking_service_users") and user.has_perm("disabling_newsletter"):
            return UserManagerForm
        raise PermissionDenied
