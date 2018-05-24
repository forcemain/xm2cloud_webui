#! -*- coding: utf-8 -*-


from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def profile(instance, raw, created, using, update_fields, **kwargs):
    from .. import models

    if created:
        models.Profile.objects.create(user=instance)
    else:
        instance.profile.save()

