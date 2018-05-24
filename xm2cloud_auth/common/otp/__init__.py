#! -*- coding: utf-8 -*-

import pyotp


class BaseOtpGenerator(object):
    otp = None

    def make_otp(self, *args, **kwargs):
        raise NotImplementedError

    def check_otp(self, *args, **kwargs):
        raise NotImplementedError


class DefaultTotpGenerator(BaseOtpGenerator):
    key_salt = pyotp.random_base32()
    otp = pyotp.TOTP(key_salt, interval=600)

    def make_otp(self):
        return self.otp.now()

    def check_otp(self, num):
        return self.otp.verify(num)


class DefaultGotpGenerator(BaseOtpGenerator):
    def make_otp(self, secret_key, user_name, issuer_name):
        otp = pyotp.totp.TOTP(secret_key)

        return otp.provisioning_uri(user_name, issuer_name=issuer_name)

    def check_otp(self, secret_key, num):
        otp = pyotp.TOTP(secret_key)
        cur_num = otp.now()

        return num == cur_num


default_otp_generator = DefaultTotpGenerator()
default_gotp_generator = DefaultGotpGenerator()
