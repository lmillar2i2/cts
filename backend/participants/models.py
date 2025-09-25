import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name="Nombre completo")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Teléfono")
    is_verified = models.BooleanField(default=False, verbose_name="Verificado")
    password = models.CharField(max_length=128, blank=True)  # guardará hash
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Se guarda la contraseña hasheada."""
        self.password = make_password(raw_password)

    def verify_password(self, raw_password):
        """Verifica si la contraseña es igual al hash almacenado."""
        return check_password(raw_password, self.password)
    
    class Meta:
        db_table = 'participants'
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} <{self.email}>"