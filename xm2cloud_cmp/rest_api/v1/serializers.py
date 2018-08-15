#! -*- coding: utf-8 -*-


from django.utils import timezone
from rest_framework import serializers


from ... import models


class ScriptSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(default=timezone.now, required=False)

    class Meta:
        model = models.Script
        exclude = ['create_time']
