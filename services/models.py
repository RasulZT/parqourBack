from django.db import models

from users.models import CustomUser

from utils.enums import CriticalityLevel, AsanaIssueStatus, TicketSection, LanguageCode
from django.utils import timezone


class Parking(models.Model):
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255,null=True,blank=True)
    ip = models.CharField(max_length=255,null=True,blank=True)
    google_table_link = models.TextField(null=True, blank=True)
    group_name = models.CharField(max_length=255)
    group_chat_id = models.BigIntegerField(null=True, blank=True)
    language_code = models.CharField(max_length=2, choices=LanguageCode.choices, default=LanguageCode.RU)


class Ticket(models.Model):
    asana_issue_id = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_tickets'  # 🔧 добавить!
    )
    parking = models.ForeignKey(Parking, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.CharField(max_length=255, null=True, blank=True)
    problem_area = models.CharField(max_length=255, null=True, blank=True)
    criticality_level = models.CharField(max_length=50, choices=CriticalityLevel.choices, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    message_id = models.IntegerField(null=True, blank=True)
    comments_updated_time = models.DateTimeField(null=True, blank=True)
    is_ticket_closed = models.BooleanField(default=False)
    asana_issue_status = models.CharField(max_length=50, choices=AsanaIssueStatus.choices, default='CREATED')
    section = models.CharField(max_length=50, choices=TicketSection.choices, default='Line - 1')


# Create your models here.
class SupportSession(models.Model):
    support = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions')
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)  # 🔄 заменили chat → parking
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.support} ⇄ {self.parking.group_name}"


class SupportMessage(models.Model):
    session = models.ForeignKey(SupportSession, on_delete=models.CASCADE, related_name="messages")

    # Отправитель
    from_user = models.JSONField(max_length=10000, null=True, blank=True)

    # Текст сообщения / подпись
    text = models.TextField(null=True, blank=True)

    # Медиа
    photo_file_id = models.CharField(max_length=512, null=True, blank=True)
    video_file_id = models.CharField(max_length=512, null=True, blank=True)
    video_note_file_id = models.CharField(max_length=512, null=True, blank=True)
    voice_file_id = models.CharField(max_length=512, null=True, blank=True)
    voice_duration = models.PositiveIntegerField(null=True, blank=True)

    # Telegram мета
    message_id = models.BigIntegerField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_from_group = models.BooleanField(default=False)
    group_chat_id = models.BigIntegerField(null=True, blank=True)
    group_title = models.CharField(max_length=255, null=True, blank=True)

    # Переслано от (если форвард)
    forward_from_user_id = models.BigIntegerField(null=True, blank=True)
    forward_from_username = models.CharField(max_length=255, null=True, blank=True)
    forward_from_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        who = self.from_user_name or self.from_username or "❓"
        preview = self.text or "[медиа]"
        return f"[{self.date.strftime('%Y-%m-%d %H:%M')}] {who}: {preview[:30]}"


class ServiceGroup(models.Model):
    name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)
    group_chat_id = models.CharField(null=True, blank=True, max_length=255)


class AsanaIssue(models.Model):
    text = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    issue_id = models.CharField(max_length=255, null=True, blank=True)
    author_resource_type = models.CharField(max_length=255, null=True, blank=True)
    author_name = models.CharField(max_length=255, null=True, blank=True)
    author_gid = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    comment_id = models.CharField(max_length=255, null=True, blank=True)
    issue_comment_id = models.CharField(max_length=255, unique=True)
    is_comment_sent = models.BooleanField(default=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='asana_comments')


class IssueComment(models.Model):
    text = models.TextField()
    deleted = models.BooleanField(default=False)
    issue_id = models.CharField(max_length=255)
    author_login = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    author_id = models.CharField(max_length=255)
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    comment_id = models.CharField(max_length=255)
    issue_comment_id = models.CharField(max_length=255, unique=True)
    is_comment_sent = models.BooleanField(default=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='youtrack_comments')


class Duty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_duties')
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_duties')
    duty_date = models.DateField()
