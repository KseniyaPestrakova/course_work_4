from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "username", 'email')


