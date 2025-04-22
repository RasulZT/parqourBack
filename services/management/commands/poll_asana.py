from django.core.management.base import BaseCommand
from services.asanaService.asana_service import AsanaService
from services.models import Ticket


class Command(BaseCommand):
    help = "Polls Asana and updates linked tickets"

    def handle(self, *args, **options):
        tickets = Ticket.objects.filter(asana_issue_id__isnull=False, is_ticket_closed=False)
        for ticket in tickets:
            asana_data = AsanaService.fetch_task_detail(ticket.asana_issue_id)
            AsanaService._process_task_detail(ticket, asana_data)

        AsanaService.fetch_tasks_and_update()
        self.stdout.write("🎯 Asana sync complete.")
