from django import forms
from .models import Subscriber, Message


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['fio', 'email', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']