from django.contrib import admin

from .models import AttemptSent, Message, Newsletter, Subscriber
from .services import run_newsletter


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "fio")
    search_fields = ("comment",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject", "body")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("start_sent_at", "finish_sent_at", "status")
    search_fields = ("status", "message")
    actions = ["start_newsletter"]

    def start_newsletter(self, request, queryset):
        for newsletter in queryset:
            run_newsletter(newsletter.pk)
        self.message_user(request, "Рассылка успешно запущена.")

    start_newsletter.short_description = "Запустить выбранные рассылки"


@admin.register(AttemptSent)
class AttemptSentAdmin(admin.ModelAdmin):
    list_display = ("created_at", "status", "server_response")
    search_fields = ("status", "server_response")
