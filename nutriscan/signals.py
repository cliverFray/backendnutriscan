from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AditionalInfoUser

""" @receiver(post_save, sender=User)
def create_cuidador_profile(sender, instance, created, **kwargs):
    if created:
        # Solo crea el perfil adicional si no existe uno para el usuario
        AditionalInfoUser.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_cuidador_profile(sender, instance, **kwargs):
    # Solo intenta guardar si el usuario tiene un perfil adicional
    if hasattr(instance, 'aditionalinfouser'):
        instance.aditionalinfouser.save() """
