# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import uuid


from django.utils import timezone
from django.db import models as db_models
from django.contrib.auth import models as auth_models


from .common.storage import generate_filename
from .signal import profile as profile_signals
from .common.db.models import StrictedImageFileField


class Profile(db_models.Model):
    address = db_models.TextField(default='', blank=True)
    phone = db_models.CharField(max_length=11, default='', blank=True)
    photo = db_models.CharField(max_length=255, default='', blank=True)
    thumbs = db_models.CharField(max_length=255, default='', blank=True)
    telephone = db_models.CharField(max_length=32, default='', blank=True)
    city = db_models.CharField(max_length=32, default=u'杭州市', blank=True)
    mfa_protect_is_enable = db_models.SmallIntegerField(default=0, blank=True)
    province = db_models.CharField(max_length=32, default=u'浙江省', blank=True)
    district = db_models.CharField(max_length=32, default=u'富阳区', blank=True)
    mfa_secret_key = db_models.CharField(max_length=16, default='', blank=True)
    nationality = db_models.CharField(max_length=32, default=u'中国', blank=True)
    mfa_gotp_qurls = db_models.CharField(max_length=255, default='', blank=True)
    update_time = db_models.DateTimeField(auto_now_add=True, blank=True)
    create_time = db_models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = db_models.CharField(max_length=36, primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    avatar = StrictedImageFileField(upload_to=generate_filename('avatars'), sizes=((99, 99),), blank=True)
    operate_protect_intensity = db_models.CharField(max_length=32,
                                                    choices=[('default', 'default'), ('force', 'force')],
                                                    default='default', blank=True)
    operate_protect_method = db_models.CharField(max_length=32,
                                                 choices=[('phone', 'phone'), ('email', 'email'), ('mfa', 'mfa')],
                                                 default='email', blank=True)

    user = db_models.OneToOneField(auth_models.User)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.photo = self.thumbs
            super(Profile, self).save(*args, **kwargs)
            return
        self.photo = self.avatar.url
        self.thumbs = self.avatar.url_99x99
        self.avatar = None
        super(Profile, self).save(*args, **kwargs)
