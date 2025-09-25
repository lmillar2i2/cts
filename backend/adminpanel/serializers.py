from rest_framework import serializers
from participants.models import Participant
from .models import Winner


class ParticipantAdminListSerializer(serializers.ModelSerializer):
    """Serializer para mostrar participantes en el panel del admin."""
    class Meta:
        model = Participant
        fields = ["id", "name", "email", "is_verified", "created_at"]


class WinnerSerializer(serializers.ModelSerializer):
    """Serializer para mostrar ganadores en el admin después de generar el sorteo"""
    participant = ParticipantAdminListSerializer(read_only=True)

    class Meta:
        model = Winner
        fields = ["id", "participant", "date_won", "notified", "valentin_version"]
