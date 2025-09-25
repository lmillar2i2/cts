from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Participant
from .serializers import ParticipantCreateSerializer, SetPasswordSerializer
from .tasks import send_verification_email

signer = TimestampSigner()


class RegisterView(APIView):
    """Registra participante y envía correo de verificación."""
    def post(self, request):
        ser = ParticipantCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]

        if Participant.objects.filter(email=email).exists():
            return Response({"detail": "Email ya registrado."}, status=400)

        p = Participant.objects.create(**ser.validated_data)
        token = signer.sign(str(p.id))
        link = f"http://localhost:5173/verify/{token}"  # URL del frontend
        try:
            send_verification_email.delay(p.email, link)
        except Exception as e:
            send_verification_email(p.email, link)
        return Response({"message": "¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta."})


class VerifyView(APIView):
    """Verifica el token de correo."""
    def get(self, request, token: str):
        try:
            pid = signer.unsign(token, max_age=60 * 60 * 24)  # Token válido por 24h
            p = Participant.objects.get(id=pid)
            p.is_verified = True
            p.save(update_fields=["is_verified"])
            return Response({"message": "Correo verificado. Ahora crea tu contraseña.", "token": token})
        except (BadSignature, SignatureExpired, Participant.DoesNotExist):
            return Response({"detail": "Token inválido o expirado."}, status=400)


class SetPasswordView(APIView):
    """Crear contraseña después de acceder al link de verificación."""
    def post(self, request):
        ser = SetPasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        token = ser.validated_data["token"]
        password = ser.validated_data["password"]

        try:
            pid = signer.unsign(token, max_age=60 * 60 * 24)
            p = Participant.objects.get(id=pid)
            p.set_password(password)
            p.save(update_fields=["password"])
            return Response({"message": "Tu cuenta ha sido activada. Ya estás participando en el sorteo."})
        except (BadSignature, SignatureExpired, Participant.DoesNotExist):
            return Response({"detail": "Token inválido o expirado."}, status=400)
