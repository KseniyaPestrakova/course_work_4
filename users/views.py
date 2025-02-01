import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView, View

from config.settings import EMAIL_HOST_USER

from .forms import CustomUserUpdateForm, UserManagerForm, UserRegisterForm
from .models import CustomUser


class BlockingUsersView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        service_user = get_object_or_404(CustomUser, id=user_id)

        if not request.user.has_perm("blocking_users"):
            return HttpResponseForbidden("У вас нет прав на блокировку пользователя")
        service_user.is_active = False
        service_user.save()

        return redirect("users:customuser_detail", pk=user_id)


class RegisterView(FormView):
    model = CustomUser
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/confirm/{token}"
        send_mail(
            subject="Подтверждение регистрации в сервисе",
            message=f"Добро пожаловать в наш сервис! Для подтверждения регистрации пройдите по ссылке ниже:\n"
            f"{url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = "customuser_detail.html"


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "register.html"
    success_url = reverse_lazy("mailing:home")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.pk:
            return CustomUser
        elif user.has_perm("blocking_users") and user.has_perm("disabling_newsletter"):
            return UserManagerForm
        raise PermissionDenied


class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "customuser_list.html"
