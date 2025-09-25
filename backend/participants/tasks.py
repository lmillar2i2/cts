from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email(to_email: str, link: str):
    """Envía correo de verificación con link al frontend. Actualmente está configurado para ver ek correo y link de verificación
    en el log del backend pero puede configurarse para usar SMTP"""
    send_mail(
        subject="Verifica tu cuenta – Sorteo San Valentín CTS",
        message=f"Hola! Verifica tu cuenta aquí: {link}",
        from_email="no-reply@cts-turismo.cl",
        recipient_list=[to_email],
        fail_silently=False,
    )
