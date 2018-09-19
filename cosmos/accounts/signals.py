from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings

from .models import User


@receiver(post_migrate, sender=None)
def create_superuser(sender, **kwargs):
    """
    Creates a new superuser if doesn't exist after every migrate action
    User details are populated from settings (
        SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD
    )
    """
    if hasattr(settings, 'CREATE_SUPERUSER') and settings.CREATE_SUPERUSER:

        email = settings.SUPERUSER_EMAIL
        password = settings.SUPERUSER_PASSWORD

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            print('Creating superuser ({0}:{1})'.format(email, password))
            User.objects.create_superuser(email=email, password=password)
