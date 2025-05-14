from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import (
    Parking, ServiceGroup, Ticket,
    AsanaIssue, IssueComment, Duty, SupportSession
)


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


class ServiceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGroup
        fields = '__all__'



class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'


class AsanaIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsanaIssue
        fields = '__all__'


class IssueCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueComment
        fields = '__all__'


class DutySerializer(serializers.ModelSerializer):
    class Meta:
        model = Duty
        fields = '__all__'


from rest_framework import serializers
from .models import SupportMessage


class SupportSessionSerializer(serializers.ModelSerializer):
    support = CustomUserSerializer()
    parking = ParkingSerializer()
    ticket = TicketSerializer()

    class Meta:
        model = SupportSession
        fields = '__all__'


class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = [
            'id',
            'session',

            'from_user',
            'text',

            'photo_file_id',
            'video_file_id',
            'video_note_file_id',
            'voice_file_id',
            'voice_duration',

            'message_id',
            'date',
            'is_from_group',
            'group_chat_id',
            'group_title',

            'forward_from_user_id',
            'forward_from_username',
            'forward_from_name',
        ]
