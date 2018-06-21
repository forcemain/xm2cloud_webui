# -*- coding: utf-8 -*-


import pika


from django.conf import settings


class BaseChannelHelper(object):
    def __init__(self, **kwargs):
        self._ssl = settings.CHANNEL_RABBITMQ_SSL
        self._host = settings.CHANNEL_RABBITMQ_HOST
        self._port = settings.CHANNEL_RABBITMQ_PORT
        self._vhost = settings.CHANNEL_RABBITMQ_VHOST
        self._queue = settings.CHANNEL_RABBITMQ_DOWN_QUEUE
        self._auth_user = settings.CHANNEL_RABBITMQ_AUTH_USER
        self._auth_pass = settings.CHANNEL_RABBITMQ_AUTH_PASS
        self._exchange = settings.CHANNEL_RABBITMQ_DOWN_EXCHANGE
        self._routing_key = settings.CHANNEL_RABBITMQ_ROUTING_KEY
        self._exchange_type = settings.CHANNEL_RABBITMQ_EXCHANGE_TYPE

    def connect(self):
        conn_parameters = pika.ConnectionParameters(
            ssl=self._ssl,
            host=self._host,
            port=self._port,
            retry_delay=5,
            channel_max=1000,
            socket_timeout=15,
            heartbeat_interval=10,
            connection_attempts=5,
            virtual_host=self._vhost,
            credentials=pika.PlainCredentials(self._auth_user, self._auth_pass),
        )
        return pika.BlockingConnection(conn_parameters)


class RabbitMQChannelSender(BaseChannelHelper):
    def __init__(self, **kwargs):
        super(RabbitMQChannelSender, self).__init__(**kwargs)

    def publish_message(self, message):
        connect = self.connect()
        channel = connect.channel()
        channel.confirm_delivery()
        channel.basic_publish(self._exchange, self._routing_key, message,
                              properties=pika.BasicProperties(delivery_mode=1))
        connect.close()



    
    

