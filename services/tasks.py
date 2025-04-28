from celery import shared_task
from services.asanaService.asana_service import AsanaService
from services.models import Ticket


@shared_task
def poll_asana_task():
    print("🔄 poll_asana_task работает",flush=True)
    tickets = Ticket.objects.filter(asana_issue_id__isnull=False, is_ticket_closed=False)
    for ticket in tickets:
        asana_data = AsanaService.fetch_task_detail(ticket.asana_issue_id)
        if asana_data:
            AsanaService._process_task_detail(ticket, asana_data)
