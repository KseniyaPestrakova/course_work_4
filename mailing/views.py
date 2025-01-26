from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import CreateView
from mailing.models import Subscriber, Message, Newsletter
from django.urls import reverse_lazy
from mailing.forms import SubscriberForm, MessageForm, NewsletterForm


class SubscriberListView(ListView):
    model = Subscriber


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = 'mailing/subscriber_detail.html'


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'mailing/subscriber_form.html'
    success_url = reverse_lazy('mailing:subscriber_list')

    def form_valid(self, form):
        subscriber = form.save()
        user = self.request.user
        subscriber.owner = user
        subscriber.save()
        return super().form_valid(form)



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


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


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

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset()


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'mailing/newsletter_detail.html'

    def get_object(self, queryset=None):
        return self.object


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = MessageForm
    template_name = 'mailing/newsletter_form.html'
    success_url = reverse_lazy('mailing:newsletter_list')

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'mailing/newsletter_form.html'
    success_url = reverse_lazy('mailing:newsletter_list')


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = "mailing/newsletter_confirm_delete.html"
    success_url = reverse_lazy("mailing:newsletter_list")


class HomeTemplateView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["count_newsletter"] = len(Newsletter.objects.all())
        active_newsletter_count = Newsletter.objects.filter(status="Запущена").count()
        context_data["active_newsletter_count"] = active_newsletter_count
        unique_subscribers_count = Subscriber.objects.distinct().count()
        context_data["unique_subscribers_count"] = unique_subscribers_count
        return context_data
