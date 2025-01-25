from django.contrib import admin
from .models import Subscriber, Message, Newsletter


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "fio")
    search_fields = ("comment",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject", "body")


@admin.register(Newsletter)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("start_sent_at", "finish_sent_at", "status")
    search_fields = ("status", "message")