from django.urls import path

from . import views
from .views import SubscriberListView, SubscriberDetailView, SubscriberCreateView, SubscriberUpdateView, \
    SubscriberDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, NewsletterDeleteView, \
    HomeTemplateView, AttemptSentListView

app_name = 'mailing'

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("subscriber/", SubscriberListView.as_view(), name="subscriber_list"),
    path("subscriber/<int:pk>/", SubscriberDetailView.as_view(), name="subscriber_detail"),
    path("subscriber/create/", SubscriberCreateView.as_view(), name="subscriber_create"),
    path("subscriber/update/<int:pk>/", SubscriberUpdateView.as_view(), name="subscriber_update"),
    path("subscriber/delete/<int:pk>/", SubscriberDeleteView.as_view(), name="subscriber_confirm_delete"),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_confirm_delete"),
    path("newsletter/", NewsletterListView.as_view(), name="newsletter_list"),
    path("newsletter/<int:pk>/", NewsletterDetailView.as_view(), name="newsletter_detail"),
    path("newsletter/create/", NewsletterCreateView.as_view(), name="newsletter_create"),
    path("newsletter/update/<int:pk>/", NewsletterUpdateView.as_view(), name="newsletter_update"),
    path("newsletter/delete/<int:pk>/", NewsletterDeleteView.as_view(), name="newsletter_confirm_delete"),
    path("attemptsent/", AttemptSentListView.as_view(), name="attemptsent_list"),
    path('newsletter/<int:newsletter_id>/launch/', views.start_newsletter_view, name='launch_newsletter'),
    ]
