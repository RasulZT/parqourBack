from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from rest_framework.views import APIView

from users.models import CustomUser
from .models import Ticket, SupportSession
from .serializers import TicketSerializer, ParkingSerializer, SupportSessionSerializer


@api_view(['POST'])
def receive_ticket(request):
    token = request.headers.get('X-API-TOKEN')

    if token != settings.JAVA_BOT_TOKEN:
        return HttpResponseForbidden("❌ Неверный токен доступа")

    serializer = TicketSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ticket = serializer.save()

    return Response({"status": "received", "ticket_id": ticket.id})


class TicketDeleteView(APIView):
    def delete(self, request, ticket_id):
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            return Response({"error": "Ticket not found"}, status=404)

        ticket.delete()
        return Response({"message": f"Ticket #{ticket_id} deleted successfully."}, status=204)


class SupportSessionsByTelegramView(APIView):
    def get(self, request):
        telegram_id = request.query_params.get("telegram_id")
        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=400)

        user = CustomUser.objects.filter(telegram_id=telegram_id).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        sessions = SupportSession.objects.filter(support=user).order_by("-started_at")
        serialized = SupportSessionSerializer(sessions, many=True).data

        return Response(serialized, status=200)


class SupportFinishedSessionsByTelegramView(APIView):
    def get(self, request):
        telegram_id = request.query_params.get("telegram_id")
        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=400)

        user = CustomUser.objects.filter(telegram_id=telegram_id, active=False).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        sessions = SupportSession.objects.filter(support=user).order_by("-started_at")
        serialized = SupportSessionSerializer(sessions, many=True).data

        return Response(serialized, status=200)


class TicketUpdateUserView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, ticket_id):
        try:
            telegram_id = request.data.get("telegram_id")
            if not telegram_id:
                return Response({"error": "telegram_id is required"}, status=400)

            ticket = Ticket.objects.filter(id=ticket_id).first()
            if not ticket:
                return Response({"error": "Ticket not found"}, status=404)

            user = CustomUser.objects.filter(telegram_id=telegram_id).first()
            if not user:
                return Response({"error": "User with this telegram_id not found"}, status=404)

            ticket.user = user
            ticket.save()

            return Response({
                "message": "User updated successfully",
                "ticket_id": ticket.id,
                "new_user_id": user.id,
                "new_user_telegram_id": user.telegram_id,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)


##Создать сессию
class SupportSessionCreateView(APIView):
    def post(self, request):
        try:
            support_telegram_id = request.data.get("support_telegram_id")
            ticket_id = request.data.get("ticket_id")

            if not support_telegram_id or not ticket_id:
                return Response({"error": "support_telegram_id and ticket_id are required"}, status=400)

            support = CustomUser.objects.filter(telegram_id=support_telegram_id).first()
            if not support:
                return Response({"error": "Support user not found"}, status=404)

            ticket = Ticket.objects.filter(id=ticket_id).first()
            if not ticket:
                return Response({"error": "Ticket not found"}, status=404)

            if not ticket.parking:
                return Response({"error": "Ticket is not linked to a parking"}, status=400)

            existing = SupportSession.objects.filter(support=support, ticket=ticket).first()
            if existing:
                return Response({"error": f"Этот тикет уже взят сапортом"}, status=409)

            parking = ticket.parking

            # создать сессию
            session = SupportSession.objects.create(
                support=support,
                parking=parking,
                ticket=ticket
            )

            # сериализовать ticket и parking
            ticket_data = TicketSerializer(ticket).data
            parking_data = ParkingSerializer(parking).data

            return Response({
                "session_id": session.id,
                "support_id": support.id,
                "support_telegram_id": support.telegram_id,
                "ticket": ticket_data,
                "parking": parking_data
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

##Вернуть все  сессии сапорта
