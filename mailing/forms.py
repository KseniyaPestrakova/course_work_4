from django import forms
from .models import Subscriber, Message, Newsletter


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['fio', 'email', 'comment']
        exclude = ('owner',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        exclude = ('owner',)


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['start_sent_at', 'finish_sent_at', 'status']
        exclude = ('owner',)