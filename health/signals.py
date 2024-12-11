from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=Module)
def add_module_to_user_on_created(sender, instance, created, **kwargs):
    if created:
       users = User.objects.all()
       
       for user in users:
           user.modules.add(instance)
           user.save()




