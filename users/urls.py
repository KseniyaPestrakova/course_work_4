from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, email_verification, CustomUserDetailView, CustomUserUpdateView
from django.contrib.auth import views as auth_views

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name='login'),
    path("logout/", LogoutView.as_view(next_page="/"), name='logout'),
    path("register/", RegisterView.as_view(), name='register'),
    path("confirm/<str:token>/", email_verification, name='confirm'),

    path("<int:pk>/", CustomUserDetailView.as_view(), name="customuser_detail"),
    path("update/<int:pk>/", CustomUserUpdateView.as_view(), name="customuser_update"),

    path('password_reset/', auth_views.PasswordResetView.as_view(email_template_name='password_reset_email.html',
                                                                 success_url='done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html",
                                                                                success_url='/users/reset/done/'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'
                                                      ), name='password_reset_complete'),
]
