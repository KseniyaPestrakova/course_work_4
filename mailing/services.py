from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config.settings import EMAIL_HOST_USER
from mailing.models import Newsletter


