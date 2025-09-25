import random
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from participants.models import Participant
from .models import Winner
from .serializers import ParticipantAdminListSerializer, WinnerSerializer
from .tasks import send_winner_email


class AdminLoginView(APIView):
    """Login admin con JWT"""
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if not user or not user.is_staff:
            return Response({"detail": "Credenciales inválidas"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})


class ParticipantsAdminListView(APIView):
    """Lista de participantes para admin."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Participant.objects.all().order_by("-created_at")
        ser = ParticipantAdminListSerializer(qs, many=True)
        return Response(ser.data)


class DrawWinnerView(APIView):
    """Admin selecciona ganador aleatorio y lo notifica."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        edition = "San Valentín 2025"
        already_won_ids = Winner.objects.filter(valentin_version=edition).values_list("participant_id", flat=True)
        eligible = Participant.objects.filter(is_verified=True).exclude(id__in=already_won_ids)

        
        count = eligible.count()
        #if not eligible.exists():
        if count == 0:
            return Response({"detail": "No hay participantes elegibles."}, status=400)

        
        random_index = random.randint(0, count - 1)
        winner = eligible[random_index]
        #winner = eligible.order_by("?").first() #Para elegir random pero es poco eficiente
        w = Winner.objects.create(participant=winner, valentin_version=edition)
        
        send_winner_email.delay(w.id,winner.email, winner.name, edition)

        ser = WinnerSerializer(w)
        return Response({"winner": ser.data}, status=201)
