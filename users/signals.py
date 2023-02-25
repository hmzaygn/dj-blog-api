from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)  # User tablosundaki işlem bittikten sonra (save olduktan sonra) işlemi başlat
def create_Token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#! signals oluşturulduktan sonra apps.py dosyasına kaydetmek gerek
