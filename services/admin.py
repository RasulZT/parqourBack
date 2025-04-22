from django.contrib import admin
from .models import (
    Parking, ServiceGroup, Ticket,
    AsanaIssue, IssueComment, Duty, SupportSession, SupportMessage
)


@admin.register(SupportSession)
class SupportSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'support',
        'parking',
        'ticket',
        'active',
        'started_at',
        'ended_at',
    )
    list_filter = ('active', 'started_at', 'ended_at')
    search_fields = ('support__telegram_fullname', 'ticket__summary', 'parking__name')
    readonly_fields = ('started_at',)

    def __str__(self, obj):
        return f"{obj.support} ⇄ {obj.parking}"

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_name', 'group_chat_id', 'language_code')
    search_fields = ('name', 'group_name')


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_name', 'group_chat_id')
    search_fields = ('name',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'parking', 'criticality_level', 'asana_issue_status', 'section', 'is_ticket_closed')
    search_fields = ('order_id', 'project')
    list_filter = ('criticality_level', 'asana_issue_status', 'section', 'is_ticket_closed')


@admin.register(AsanaIssue)
class AsanaIssueAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'issue_id', 'created_at', 'deleted', 'is_comment_sent')
    search_fields = ('author_name', 'issue_id')


@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'issue_id', 'comment_id', 'deleted', 'is_comment_sent')
    search_fields = ('author_name', 'comment_id')


@admin.register(Duty)
class DutyAdmin(admin.ModelAdmin):
    list_display = ('user', 'assigned_user', 'duty_date')
    list_filter = ('duty_date',)

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'session',
        'display_from_user',
        'short_text',
        'has_photo',
        'has_video',
        'has_voice',
        'has_video_note',
        'date',
        'is_from_group',
        'group_title',
    )

    list_filter = ('is_from_group', 'date', 'session')
    search_fields = ('text', 'group_title')
    readonly_fields = ('date',)

    def display_from_user(self, obj):
        if not obj.from_user:
            return "—"
        name = obj.from_user.get("first_name", "")
        last = obj.from_user.get("last_name", "")
        return f"{name} {last}".strip()
    display_from_user.short_description = "Отправитель"

    def short_text(self, obj):
        return (obj.text[:50] + "...") if obj.text and len(obj.text) > 50 else obj.text or "—"
    short_text.short_description = "Текст"

    def has_photo(self, obj):
        return bool(obj.photo_file_id)
    has_photo.boolean = True
    has_photo.short_description = "Фото"

    def has_video(self, obj):
        return bool(obj.video_file_id)
    has_video.boolean = True
    has_video.short_description = "Видео"

    def has_voice(self, obj):
        return bool(obj.voice_file_id)
    has_voice.boolean = True
    has_voice.short_description = "Голос"

    def has_video_note(self, obj):
        return bool(obj.video_note_file_id)
    has_video_note.boolean = True
    has_video_note.short_description = "Видео-заметка"