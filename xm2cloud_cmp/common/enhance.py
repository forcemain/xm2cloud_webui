#! -*- coding: utf-8 -*-


import re
import os
import uuid
import psutil
import signal
import shutil
import hashlib
import chardet


class ExtStr(str):
    def __init__(self, *args, **kwargs):
        super(ExtStr, self).__init__()

    def exact(self, data):
        return self == data

    def not_exact(self, data):
        return not self.exact(data)

    def iexact(self, data):
        return self.lower() == data.lower()

    def not_iexact(self, data):
        return not self.iexact(data)

    def contains(self, data):
        return data in self

    def not_contains(self, data):
        return not self.contains(data)

    def icontains(self, data):
        return data.lower() in self.lower()

    def not_icontains(self, data):
        return not self.icontains(data)

    def not_startswith(self, data):
        return not self.startswith(data)

    def istartswith(self, data):
        return self.lower().startswith(data.lower())

    def not_istartswith(self, data):
        return not self.istartswith(data)

    def not_endswith(self, data):
        return not self.endswith(data)

    def iendswith(self, data):
        return self.lower().endswith(data.lower())

    def not_iendswith(self, data):
        return not self.iendswith(data)

    def regexp(self, data):
        return re.search(data, self)

    def not_regexp(self, data):
        return not self.regexp(data)


class ExtDict(dict):
    def __getattr__(self, item):
        return super(ExtDict, self).__getitem__(item)


class File(object):
    @staticmethod
    def force_move(spath, dpath):
        if not os.path.exists(spath):
            return

        basedir = os.path.dirname(dpath)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        shutil.move(spath, dpath)

    @staticmethod
    def get_str_md5(data):
        md5 = hashlib.md5()
        md5.update(data)

        return md5.hexdigest()

    @staticmethod
    def read_content(path):
        content = ''
        with open(path, 'r+b') as fd:
            for line in fd:
                content += line

        return content

    @staticmethod
    def write_content(data, path):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(path, 'w+b') as fd:
            fd.write(data)

    @staticmethod
    def get_file_md5(path):
        md5 = hashlib.md5()

        with open(path, 'r+b') as fd:
            for line in fd:
                md5.update(line)

        return md5.hexdigest()

    @staticmethod
    def set_file_utf8(path):
        detector = chardet.UniversalDetector()
        with open(path, 'r+b') as fd:
            for line in fd:
                detector.feed(line)
                if detector.done:
                    break

        detector.close()
        encoding = detector.result['encoding']

        dirname, _, basename = path.rpartition(os.sep)
        new_file = os.path.join(dirname, '.{0}'.format(basename))
        with open(new_file, 'a+b') as _fd:
            with open(path, 'r+b') as fd:
                for line in fd:
                    encoded_data = line.decode(encoding).encode('utf-8')
                    _fd.write(encoded_data)

        shutil.move(new_file, path)


class Switch(object):
    def __init__(self, v):
        self._v = v

    def __iter__(self):
        yield self.case

    def case(self, *args):
        if len(args) == 0:
            return True

        return self._v in args


class Random(object):
    @staticmethod
    def get_uuid():
        return uuid.uuid4().__str__()

get_uuid = Random.get_uuid

