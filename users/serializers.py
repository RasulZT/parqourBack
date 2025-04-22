from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'telegram_id', 'telegram_fullname',
            'full_name', 'phone_number', 'language_code', 'parkings',
            'operators', 'role', 'groups', 'user_permissions'
        ]


class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    telegram_fullname = serializers.CharField()

    def validate(self, data):
        telegram_id = data.get("telegram_id")
        fullname = data.get("telegram_fullname")

        if not telegram_id or not fullname:
            raise serializers.ValidationError("Нужны telegram_id и telegram_fullname")

        return data
