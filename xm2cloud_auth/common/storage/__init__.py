#! -*- coding: utf-8 -*-


import os
import uuid


from datetime import datetime
from functools import partial


def upload_to(path, instance, filename):
    dir_name = datetime.now().strftime('{0}/%Y/%m/%d'.format(path))
    basename = '{0}{1}'.format(uuid.uuid4().__str__(), os.path.splitext(filename)[-1])
    filepath = os.path.join(dir_name, basename)

    return filepath


def generate_filename(path=None):
    path = path if path else 'attachments'

    return partial(upload_to, path)
