from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'title', 'type', 'object_name')
    search_fields = ('title', 'object_name')

