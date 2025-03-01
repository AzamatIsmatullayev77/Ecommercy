from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

from config import settings
from .models import Product, Customer, ProductImage, ProductAttribute


@receiver(post_save, sender=Customer)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Xush kelibsiz!',
            f'Hurmatli {instance.name}, siz tizimga muvaffaqiyatli ro‘yxatdan o‘tdingiz!',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    if created:
        print(f"Yangi mahsulot qo'shildi: {instance.name}")


@receiver(post_save, sender=ProductImage)
def product_image_added(sender, instance, created, **kwargs):
    if created:
        print(f"{instance.product.name} mahsulotiga yangi rasm qo‘shildi.")

