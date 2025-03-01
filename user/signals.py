from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Faqat yangi foydalanuvchi yaratilganda
        send_mail(
            'Xush kelibsiz!',
            'Siz saytga kirdingiz.',
            settings.EMAIL_HOST_USER,  # Kimdan
            [instance.email],  # Kimga
            fail_silently=False,
        )
