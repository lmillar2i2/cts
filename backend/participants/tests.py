from django.test import TestCase
from rest_framework.test import APIClient
from participants.models import Participant

class ParticipantTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    """Test para registro participantes"""
    def test_register_participant_success(self):
        data = {"name": "Juan Pérez", "email": "juan@ejemplo.com", "phone": "123456"}
        response = self.client.post("/api/register/", data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Gracias por registrarte", response.data["message"])

        p = Participant.objects.get(email="juan@ejemplo.com")
        self.assertEqual(p.name, "Juan Pérez")
        self.assertFalse(p.is_verified)

    """Test para verificar duplicado de email"""
    def test_register_participant_duplicate_email(self):
        Participant.objects.create(name="Test", email="juan@ejemplo.com", phone="123")
        data = {"name": "Otro", "email": "juan@ejemplo.com", "phone": "555"}
        response = self.client.post("/api/register/", data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get("detail"), "Email ya registrado.")


