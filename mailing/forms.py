from django import forms

from .models import Message, Newsletter, Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["fio", "email", "comment"]
        exclude = ("owner",)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        exclude = ("owner",)


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["status", "message", "subscribers"]
        exclude = ("owner", "start_sent_at", "finish_sent_at")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields["message"].queryset = Message.objects.all()
            self.fields["message"].label = "Выберите сообщение"
            self.fields["message"].widget = forms.Select(attrs={"class": "form-control"})

            self.fields["subscribers"].queryset = Subscriber.objects.all()
            self.fields["subscribers"].label = "Выберите получателей"
            self.fields["subscribers"].widget = forms.SelectMultiple(attrs={"class": "form-control"})


class NewsletterManagerForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = [
            "status",
        ]
