from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from ...models import Notification

class Command(BaseCommand):
    help = 'Enviar recordatorios mensuales a los cuidadores'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        today = timezone.now().date()

        for user in users:
            last_notification = Notification.objects.filter(user=user).order_by('-notificationDate').first()
            
            # Enviar recordatorio si no ha recibido uno en el último mes
            if not last_notification or last_notification.notificationDate < today - timedelta(days=30):
                Notification.objects.create(
                    notificationTitle="Recordatorio mensual",
                    notificationDescription="Por favor, actualiza la información de tu hijo en la aplicación.",
                    user=user
                )
                self.stdout.write(self.style.SUCCESS(f"Notificación enviada a {user.username}"))
