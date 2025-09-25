from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction
from .models import Winner
from django.utils.timezone import now

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_winner_email(winner_id, to_email, name, edition):
    """Envía correo al ganador del sorteo."""
    send_mail(
        subject=f"¡Has ganado el sorteo {edition}!",
        message=f"Felicitaciones {name}, ganaste la estadía de 2 noches en el hotel",
        from_email="no-reply@cts-turismo.cl",
        recipient_list=[to_email],
        fail_silently=False,
    )
   
    # Asegurar que solo se marque si el ganador fue notificado si el envío fue exitoso
    with transaction.atomic():
        w = Winner.objects.select_for_update().get(id=winner_id)
        w.notified = True
        w.notified_at = now()
        w.save(update_fields=["notified", "notified_at"])