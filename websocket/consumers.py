import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "ticket_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Этот consumer только получает от сервера → ничего не обрабатываем от клиента
        pass

    async def send_ticket(self, event):
        # Отправляем клиенту данные о тикете
        await self.send(text_data=json.dumps(event["message"]))

    async def ticket_deleted(self, event):
        await self.send(text_data=json.dumps({
            "event": "ticket_deleted",
            "data": event["message"]
        }))

    async def ticket_updated(self, event):
        await self.send(text_data=json.dumps({
            "event": "ticket_updated",
            "data": event["message"]
        }))
