from rest_framework import serializers
from .models import Participant


class ParticipantCreateSerializer(serializers.ModelSerializer):
    """Serializer para registro inicial (sin password)."""
    email = serializers.EmailField(validators=[]) #Se quita el validador de unicidad del DRF para manejar el error de duplicado en la vista
    phone = serializers.RegexField( #Se agrega validador de formato simple 
        regex=r'^\+569\d{8}$',
        required=False,
        allow_blank=True,
        error_messages={
            "invalid": "El número debe tener el formato +569XXXXXXXX"
        }
    )
    class Meta:
        model = Participant
        fields = ["name", "email", "phone"]


class ParticipantListSerializer(serializers.ModelSerializer):
    """Serializer para listar participantes (admin)."""
    class Meta:
        model = Participant
        fields = ["id", "name", "email", "is_verified", "created_at"]


class SetPasswordSerializer(serializers.Serializer):
    """Serializer para creación de contraseña tras verificación."""
    token = serializers.CharField()
    password = serializers.CharField(min_length=6)
