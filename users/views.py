from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import TelegramAuthSerializer, CustomUserSerializer


class TelegramAuthView(APIView):
    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id = serializer.validated_data['telegram_id']
        fullname = serializer.validated_data['telegram_fullname']
        status = "exist"
        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "telegram_fullname": fullname
            }
        )

        if created:
            status = "new"

        if not created and not user.telegram_fullname:
            user.telegram_fullname = fullname
            user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "telegram_id": user.telegram_id,
            "role": user.role,
            "status": status
        })


class UsersByRoleView(APIView):
    def post(self, request):
        role = request.data.get('role')
        if not role:
            return Response({'error': 'Role is required'}, status=status.HTTP_400_BAD_REQUEST)

        users = CustomUser.objects.filter(role=role)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
