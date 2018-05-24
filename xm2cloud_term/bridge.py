#! -*- coding: utf-8 -*-


import paramiko


from channels.exceptions import WebsocketCloseException
from paramiko.ssh_exception import SSHException, PasswordRequiredException

from .utils import Switch
from .ioloop import IOLoop


IOLoop.instance().start()


class Credential(object):
    def __init__(self, **kwargs):
        self.instance = kwargs.get('instance', None)
        self.protocol = kwargs.get('protocol', None)

    def auth(self):
        raise NotImplementedError


class SSHCredential(Credential):
    def load_priviate_key(self, key_obj, password=''):
        try:
            pkey = paramiko.RSAKey.from_private_key(key_obj, password=password)
        except (IOError, PasswordRequiredException, SSHException):
            pkey = paramiko.DSSKey.from_private_key(key_obj, password=password)

        return pkey

    def get_ssh_host(self, host):
        return host.iplines.filter(is_preferred=True).first()

    def auth(self):
        from xm2cloud_cmp.models import Host

        host_queryset = Host.objects.filter(pk=self.instance)
        if not host_queryset:
            return {}
        host = host_queryset.first()

        for case in Switch(host.auth.authtype):
            if case('password'):
                crendent = {
                    'port': host.ssh_port,
                    'username': host.auth.username,
                    'password': host.auth.password,
                    'hostname': self.get_ssh_host(host),
                }
                return crendent
            if case('authfile'):
                pkey = self.load_priviate_key(host.auth.authfile, host.auth.authpass)
                crendent = {
                    'port': host.ssh_port,
                    'username': host.auth.username,
                    'pkey': pkey,
                    'hostname': self.get_ssh_host(host),
                }
                return crendent
            if case():
                return {}


class Bridge(object):
    def __init__(self, channel):
        self._id = None
        self._shell = None
        self._terminal = None
        self._channel = channel

    @property
    def id(self):
        return self._id

    @property
    def shell(self):
        return self._shell

    @property
    def terminal(self):
        return self._terminal

    @property
    def channel(self):
        return self._channel

    def auth(self, **kwargs):
        raise NotImplementedError

    def open(self, **kwargs):
        raise NotImplementedError

    def ioloop_register(self):
        IOLoop.instance().register(self)
        IOLoop.instance().add_future(self.terminal_to_web())

    def invoke_shell(self, **kwargs):
        raise NotImplementedError

    def web_to_terminal_send(self, data):
        raise NotImplementedError

    def terminal_to_web_send(self, data):
        raise NotImplementedError

    def web_to_terminal(self, data):
        self.web_to_terminal_send(data)

    def terminal_to_web(self):
        yield self._id
        is_connected = True
        while is_connected:
            result = yield
            if self._channel:
                try:
                    self.terminal_to_web_send(result)
                except WebsocketCloseException:
                    is_connected = False
        self.destroy()

    def destroy(self):
        if not self._terminal:
            return 
        self._terminal.close()


class SSHBridge(Bridge):
    def __init__(self, channel):
        super(SSHBridge, self).__init__(channel)
        self._terminal = paramiko.SSHClient()
        self._terminal.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def auth(self, **kwargs):
        return SSHCredential(**kwargs).auth()

    def open(self, **kwargs):
        credent = self.auth(**kwargs)
        self._terminal.connect(**credent)

        self.invoke_shell(**kwargs)
        self.ioloop_register()

    def invoke_shell(self, **kwargs):
        terminal_term = kwargs.get('term', 'xterm')
        terminal_cols = int(kwargs.get('width', 80))
        terminal_rows = int(kwargs.get('height', 24))
        self._shell = self._terminal.invoke_shell(
            term=terminal_term, width=terminal_cols,
            height=terminal_rows
        )
        self._shell.setblocking(0)
        self._id = self._shell.fileno()

    def web_to_terminal_send(self, data):
        if not self._shell:
            return
        self._shell.send(data)

    def terminal_to_web_send(self, data):
        channel_data = {'text': data}
        self._channel.send(channel_data)


class BridgeFactory(type):
    def __new__(cls, *args, **kwargs):
        protocol = kwargs.get('protocol', 'ssh')

        return {'ssh': SSHBridge}.get(protocol, SSHBridge)
