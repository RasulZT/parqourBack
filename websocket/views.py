from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save,post_delete
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