from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from django.views.generic.edit import CreateView

from mailing.forms import MessageForm, NewsletterForm, NewsletterManagerForm, SubscriberForm
from mailing.models import AttemptSent, Message, Newsletter, Subscriber
from mailing.services import run_newsletter


class DisablingNewsletter(LoginRequiredMixin, View):
    def post(self, request, newsletter_id):
        newsletter = get_object_or_404(Newsletter, id=newsletter_id)

        if not request.user.has_perm("disabling_newsletter"):
            return HttpResponseForbidden("У вас нет прав на отключение рассылки")
        newsletter.status = Newsletter.DISABLED
        newsletter.save()

        return redirect("mailing:newsletter_detail", pk=newsletter_id)


class SubscriberListView(LoginRequiredMixin, ListView):
    model = Subscriber

    def get_queryset(self):
        queryset = cache.get("subscriber_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("subscriber_queryset", queryset, 60 * 5)
        return queryset


@method_decorator(cache_page(60 * 5), name="dispatch")
class SubscriberDetailView(LoginRequiredMixin, DetailView):
    model = Subscriber
    template_name = "mailing/subscriber_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if self.request.user == self.object.owner:
            return self.object
        elif user.is_manager is True:
            return self.object
        raise PermissionDenied


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = "mailing/subscriber_form.html"
    success_url = reverse_lazy("mailing:subscriber_list")

    def form_valid(self, form):
        subscriber = form.save()
        user = self.request.user
        subscriber.owner = user
        subscriber.save()
        return super().form_valid(form)


class SubscriberUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = "mailing/subscriber_form.html"
    success_url = reverse_lazy("mailing:subscriber_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class SubscriberDeleteView(LoginRequiredMixin, DeleteView):
    model = Subscriber
    template_name = "mailing/subscriber_confirm_delete.html"
    success_url = reverse_lazy("mailing:subscriber_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = cache.get("message_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("message_queryset", queryset, 60 * 5)
        return queryset


@method_decorator(cache_page(60 * 5), name="dispatch")
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message_detail.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    def get_queryset(self):
        queryset = cache.get("newsletter_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("newsletter_queryset", queryset, 60 * 5)
        return queryset


@method_decorator(cache_page(60 * 5), name="dispatch")
class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter
    template_name = "mailing/newsletter_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if self.request.user == self.object.owner:
            return self.object
        elif user.is_manager is True:
            return self.object
        raise PermissionDenied


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = "mailing/newsletter_form.html"
    success_url = reverse_lazy("mailing:newsletter_list")

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = "mailing/newsletter_form.html"
    success_url = reverse_lazy("mailing:newsletter_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return NewsletterForm
        elif user.has_perm("blocking_service_users") and user.has_perm("disabling_newsletter"):
            return NewsletterManagerForm
        raise PermissionDenied

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    template_name = "mailing/newsletter_confirm_delete.html"
    success_url = reverse_lazy("mailing:newsletter_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class AttemptSentListView(LoginRequiredMixin, ListView):
    model = AttemptSent
    template_name = "mailing/attemptsent_list.html"

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset()


def start_newsletter_view(request, newsletter_id):

    if request.method == "POST":
        newsletter = get_object_or_404(Newsletter, id=newsletter_id)
        run_newsletter(newsletter_id)
        messages.success(request, f"Рассылка {newsletter_id} успешно запущена.")
        return redirect(reverse("mailing:newsletter_list"))
    else:
        return redirect(reverse("mailing:newsletter_list"))


class HomeTemplateView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data["count_newsletter"] = len(Newsletter.objects.all())

        active_newsletter_count = Newsletter.objects.filter(status="Запущена").count()

        context_data["active_newsletter_count"] = active_newsletter_count

        unique_subscribers_count = Subscriber.objects.distinct().count()
        context_data["unique_subscribers_count"] = unique_subscribers_count

        successful_newsletter_count = AttemptSent.objects.filter(owner=user, status="Успешно").count()
        context_data["successful_newsletter_count"] = successful_newsletter_count

        not_successful_newsletter_count = AttemptSent.objects.filter(owner=user, status="Не успешно").count()
        context_data["not_successful_newsletter_count"] = not_successful_newsletter_count

        sent_messages = AttemptSent.objects.filter(owner=user).values("newsletter__message").distinct().count()
        context_data["sent_messages"] = sent_messages

        return context_data
