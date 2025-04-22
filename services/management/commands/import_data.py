from django.core.management.base import BaseCommand
import pandas as pd
from services.models import Parking

class Command(BaseCommand):
    help = "Импорт данных из Excel в модель Parking"

    def handle(self, *args, **kwargs):
        df = pd.read_excel("services/management/commands/parkings_2.xlsx")

        created = 0
        for _, row in df.iterrows():
            Parking.objects.create(
                name=row["name"],
                host=row["host"],
                ip=row["ip"],
                group_name=row.get("group_name", ""),
                group_chat_id=row.get("group_chat_id") if pd.notna(row.get("group_chat_id")) else None,
                language_code=row.get("language_code", "ru")
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Успешно загружено {created} парковок"))
