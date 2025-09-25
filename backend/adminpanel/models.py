from django.db import models

#Tabla para guardar ganadores del sorteo
class Winner(models.Model):
    participant = models.ForeignKey("participants.Participant",on_delete=models.CASCADE,related_name="wins",verbose_name="Participante ganador")
    date_won = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de sorteo")
    notified = models.BooleanField(default=False, verbose_name="Notificado")
    notified_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de notificación")
    valentin_version = models.CharField(max_length=50, default="San Valentín 2025",verbose_name="Edición del sorteo")
    
    class Meta:
        db_table = 'winners'
        verbose_name = 'Ganador'
        verbose_name_plural = 'Ganadores'
        ordering = ['-date_won']
        unique_together = ['participant', 'valentin_version']
    
    def mark_as_notified(self):
        """Función para marcar al ganador como notificado."""
        from django.utils.timezone import now
        self.notified = True
        self.notified_at = now()
        self.save()
        
    def __str__(self):
        return f"{self.participant.email} @ {self.date_won.isoformat()}"