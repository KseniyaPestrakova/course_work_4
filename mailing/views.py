from django.shortcuts import render
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, View
from django.views.generic.edit import CreateView
from mailing.models import Subscriber, Message, Newsletter
from django.urls import reverse_lazy
from mailing.forms import SubscriberForm, MessageForm


class SubscriberListView(ListView):
    model = Subscriber


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = 'mailing/subscriber_detail.html'


class SubscriberCreateView(CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'mailing/subscriber_form.html'
    success_url = reverse_lazy('mailing:subscriber_list')


class SubscriberUpdateView(UpdateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'mailing/subscriber_form.html'
    success_url = reverse_lazy('mailing:subscriber_list')


class SubscriberDeleteView(DeleteView):
    model = Subscriber
    template_name = "mailing/subscriber_confirm_delete.html"
    success_url = reverse_lazy("mailing:subscriber_list")


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class NewsletterListView(ListView):
    model = Newsletter


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'mailing/newsletter_detail.html'


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = MessageForm
    template_name = 'mailing/newsletter_form.html'
    success_url = reverse_lazy('mailing:newsletter_list')


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = MessageForm
    template_name = 'mailing/newsletter_form.html'
    success_url = reverse_lazy('mailing:newsletter_list')


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = "mailing/newsletter_confirm_delete.html"
    success_url = reverse_lazy("mailing:newsletter_list")