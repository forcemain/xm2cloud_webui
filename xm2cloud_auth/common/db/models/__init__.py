#! -*- coding: utf-8 -*-


from functools import partial


from django.db.models import FileField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_thumbs.db.models import ImageWithThumbsField


_error_messages = {
    'invalid_content_type': _('ContentType %(content_type)s is not allowed.'),
    'invalid_image_size': _('Out of the allowed image size 200x200.'),
    'invalid_upload_size': _('Out of the allowd upload size %(max_upload_size)s.')
}


def valid_image_size(max_width_size, max_height_size, error_messages, value):
    obj = value.file

    if not hasattr(obj, 'image'):
        return
    if obj.image.size <= (max_width_size, max_height_size):
        return
    raise ValidationError(error_messages['invalid_image_size'])


def valid_upload_size(max_upload_size, error_messages, value):
    obj = value.file

    if not max_upload_size or obj.size <= max_upload_size:
        return
    raise ValidationError(error_messages['invalid_upload_size'], max_upload_size)


def valid_content_type(content_types, error_messages, value):
    obj = value.file

    if not content_types or obj.content_type in content_types:
        return
    raise ValidationError(error_messages['invalid_content_type'], obj.content_type)


class StrictedFileField(FileField):
    def __init__(self, *args, **kwargs):
        super(StrictedFileField, self).__init__(*args, **kwargs)
        self.content_types = kwargs.get('content_types', None)
        self.max_upload_size = kwargs.get('max_upload_size', None)

        self.error_messages.update(_error_messages)
        self._validators.extend([
            partial(valid_content_type, self.content_types, self.error_messages),
            partial(valid_upload_size, self.max_upload_size, self.error_messages),
        ])


class StrictedImageFileField(ImageWithThumbsField):
    def __init__(self, *args, **kwargs):
        super(StrictedImageFileField, self).__init__(*args, **kwargs)
        self.content_types = kwargs.get('content_types', None)
        self.max_width_size = kwargs.get('max_width_size', 200)
        self.max_height_size = kwargs.get('max_height_size', 200)
        self.max_upload_size = kwargs.get('max_upload_size', None)

        self.error_messages.update(_error_messages)
        self._validators.extend([
            partial(valid_content_type, self.content_types, self.error_messages),
            partial(valid_image_size, self.max_width_size, self.max_height_size, self.error_messages),
            partial(valid_upload_size, self.max_upload_size, self.error_messages),
        ])


