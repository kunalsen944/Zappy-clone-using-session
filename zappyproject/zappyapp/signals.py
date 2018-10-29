from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from zappyapp.models import Customer


@receiver(post_save, sender=User)
def create_customers(sender, instance, created, **kwargs):
    if created:
        Customer.objects.get_or_create(customer=instance)
