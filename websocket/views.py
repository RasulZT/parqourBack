from datetime import datetime

import msgpack
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from services.models import Ticket  # Импортируй свою модель корректно


@receiver(post_save, sender=Ticket)
def ticket_created_handler(sender, instance, created, **kwargs):
    print("TUT", flush=True)

    if created:
        channel_layer = get_channel_layer()

        # Получаем данные пользователя и парковки
        user = instance.user
        parking = instance.parking

        async_to_sync(channel_layer.group_send)(
            "ticket_group",
            {
                "type": "send_ticket",
                "message": {
                    "id": instance.id,
                    "asana_issue_id": instance.asana_issue_id,
                    "project": instance.project,
                    "problem_area": instance.problem_area,
                    "criticality_level": instance.criticality_level,
                    "summary": instance.summary,
                    "description": instance.description,
                    "asana_issue_status": instance.asana_issue_status,
                    "section": instance.section,
                    "is_ticket_closed": instance.is_ticket_closed,

                    # 👤 Пользователь (если есть)
                    "user": {
                        "id": user.id,
                        "telegram_id": user.telegram_id,
                        "telegram_fullname": user.telegram_fullname,
                        "role": user.role,
                        "phone": user.phone,
                        "kaspi_phone": user.kaspi_phone,
                        "address": user.address,
                        "bonus": user.bonus,
                    } if user else None,

                    # 🅿️ Паркинг (если есть)
                    "parking": {
                        "id": parking.id,
                        "name": parking.name,
                        "host": parking.host,
                        "ip": parking.ip,
                        "group_name": parking.group_name,
                        "group_chat_id": parking.group_chat_id,
                    } if parking else None
                }
            }
        )


@receiver(post_delete, sender=Ticket)
def ticket_deleted_handler(sender, instance, **kwargs):
    print("TICKET DELETED", flush=True)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "ticket_group",
        {
            "type": "ticket_deleted",
            "message": {
                "id": instance.id,
                "status": "deleted"
            }
        }
    )


@receiver(pre_save, sender=Ticket)
def save_old_ticket_state(sender, instance, **kwargs):
    if instance.pk:
        instance._previous_state = Ticket.objects.get(pk=instance.pk)


@receiver(post_save, sender=Ticket)
def send_ticket_update(sender, instance, **kwargs):
    previous_state = getattr(instance, '_previous_state', None)
    if previous_state:
        changes = {}
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(previous_state, field_name)
            new_value = getattr(instance, field_name)

            if isinstance(old_value, datetime):
                old_value = old_value.isoformat()
            if isinstance(new_value, datetime):
                new_value = new_value.isoformat()

            if old_value != new_value:
                changes[field_name] = {
                    "old": old_value,
                    "new": new_value
                }

        if changes:
            channel_layer = get_channel_layer()
            message = {
                "ticket_id": instance.id,
                "full_ticket": {
                    "asana_issue_id": instance.asana_issue_id,
                    "summary": instance.summary,
                    "description": instance.description,
                    "criticality_level": instance.criticality_level,
                    "problem_area": instance.problem_area,
                    "project": instance.project,
                    "section": instance.section,
                    "is_ticket_closed": instance.is_ticket_closed,
                    "asana_issue_status": instance.asana_issue_status,
                    "comments_updated_time": instance.comments_updated_time.isoformat() if instance.comments_updated_time else None,
                },
                "changes": changes,
            }

            async_to_sync(channel_layer.group_send)(
                'ticket_group',  # 🔥 используем ту же группу!
                {
                    'type': 'ticket_updated',  # тип обработчика в consumer
                    'message': message
                }
            )
