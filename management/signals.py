from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
import os

from .models import CustomUser


@receiver(post_migrate)
def assign_permissions_to_groups(sender, **kwargs):
    if sender.name == "management":
        Group.objects.get_or_create(name="Administrador")
        Group.objects.get_or_create(name="Instructor")


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == "management":
        if not CustomUser.objects.filter(email=os.getenv("ADMIN_USER")).exists():
            CustomUser.objects.create_superuser(os.getenv("ADMIN_USER"), 'adsocpya', 'admin', os.getenv("ADMIN_PASSWORD"))
