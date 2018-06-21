#! -*- coding: utf-8 -*-


import uuid
from celery import Task


from .models import ScriptLog
from .mixins import ExecuteScriptMixin
from .common.rabbitmq import RabbitMQChannelSender


class _ExecutorTimedTask(Task, ExecuteScriptMixin):
    ignore_result = True
    result_model = ScriptLog
    name = 'executor.timedtask'
    sender_class = RabbitMQChannelSender

    def get_parameter_data(self):
        triggermode = 1
        owner = self.get_owner()
        script = self.get_script()
        timedtask = self.get_timedtask()
        script_name = script and script.name or u'自定义脚本'
        user_script = script and script.contents or self.data_source.get('user_script', '')

        return {
            'owner': owner, 'script': script, 'timedtask': timedtask, 'triggermode': triggermode,
            'script_name': script_name, 'user_script': user_script,
        }

    def run(self, *args, **kwargs):
        self.data_source = kwargs
        eventsender = self.get_sender()
        sevent_uuid = uuid.uuid4().__str__()
        public_event, target_hosts = self.get_instances_data(sevent_uuid)

        self.result_model.objects.bulk_create(target_hosts)
        eventsender.publish_message(public_event.to_json())
