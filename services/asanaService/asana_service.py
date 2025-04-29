from services.models import Ticket  # путь под себя
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
import requests
from datetime import datetime

ASANA_TOKEN = "2/1209378764634369/1209386664849549:ba14bfd4b13f2d48d01dc386bdca79db"
BASE_URL = "https://app.asana.com/api/1.0"
WORKSPACE_ID = "1203611204418108"
PROJECT_ID = "1209269161730390"

HEADERS = {
    "Authorization": f"Bearer {ASANA_TOKEN}"
}


class AsanaService:
    # @staticmethod
    # def fetch_tasks_and_update():
    #     url = f"{BASE_URL}/projects/{PROJECT_ID}/tasks"
    #     params = {
    #         "opt_fields": "gid,name,completed,modified_at,memberships,status",
    #         "limit": 100
    #     }
    #
    #     next_page = None
    #     total = 0
    #
    #     while True:
    #         if next_page:
    #             url = next_page
    #             params = None
    #
    #         response = requests.get(url, headers=HEADERS, params=params)
    #         if response.status_code != 200:
    #             print(f"[AsanaService] Error fetching tasks: {response.text}")
    #             break
    #
    #         data = response.json()
    #         all_tasks = data.get("data", [])
    #         tasks = []
    #         for num, task in enumerate(all_tasks):
    #             if task.get("completed") == False and str(task.get("name")).startswith("[INCIDENT]"):
    #                 tasks.append(task)
    #
    #         total += len(all_tasks)
    #
    #         for task in tasks:
    #             AsanaService._process_task(task)
    #         next_page_data = data.get("next_page")
    #         next_page = next_page_data.get("uri") if next_page_data else None
    #
    #         if not next_page:
    #             break
    #
    #     print(f"[AsanaService] ✅ Synced {total} tasks.")

    def fetch_task_detail(task_gid):
        url = f"{BASE_URL}/tasks/{task_gid}"
        params = {
            "opt_fields": (
                "gid,name,notes,created_at,modified_at,completed,completed_at,due_on,due_at,"
                "assignee.name,assignee.email,"
                "projects.name,"
                "memberships.section.name,"
                "custom_fields.name,custom_fields.type,custom_fields.enum_value.name,custom_fields.number_value,"
                "followers.name,"
                "tags.name,"
                "dependencies,dependents"
            )
        }
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json().get("data")

        return data

    @staticmethod
    def _process_task_detail(ticket, asana_data):
        updated = False
        print(f"fetch Ticket:{ticket} ", flush=True)
        name = asana_data.get("name")
        notes = asana_data.get("notes")
        completed = asana_data.get("completed", False)
        modified_at = parse_datetime(asana_data.get("modified_at"))
        if modified_at and not modified_at.tzinfo:
            modified_at = make_aware(modified_at)

        # section (вложено в memberships)
        section = None
        memberships = asana_data.get("memberships", [])
        if memberships:
            section_data = memberships[0].get("section")
            section = section_data.get("name") if section_data else None

        print(f"HERE:asana_section:{section},my_Section:{ticket.section} ",flush=True)

        if section and ticket.section != section:
            ticket.section = section
            updated = True

        if updated:
            ticket.save()
            print(f"🔄 Ticket #{ticket.id} updated from Asana")
