#! -*- coding: utf-8 -*-


import uuid
from celery import Task


from .common.trigger.exception import TriggerError
from .common.rabbitmq import RabbitMQChannelSender
from .models import ScriptLog, UpdateLog, AlarmHistory
from .mixins import ExecuteScriptMixin, UpdateUserDataMixin, AnalyseTriggerMixin


class ExecutorTimedTask(Task, ExecuteScriptMixin):
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
        sevent_uuid = uuid.uuid4().__str__()
        public_event, target_hosts = self.get_instances_data(sevent_uuid)

        with self.get_sender() as eventsender:
            self.result_model.objects.bulk_create(target_hosts)
            eventsender.publish_message(public_event.to_json())


class ExecutorUpdateUserData(Task, UpdateUserDataMixin):
    ignore_result = True
    result_model = UpdateLog
    name = 'executor.updateuserdata'
    sender_class = RabbitMQChannelSender

    def run(self, *args, **kwargs):
        self.data_source = kwargs
        sevent_uuid = uuid.uuid4().__str__()
        target_events, target_hosts = self.get_instances_data(sevent_uuid)

        with self.get_sender() as eventsender:
            self.result_model.objects.bulk_create(target_hosts)
            map(lambda e: eventsender.publish_message(e.to_json()), target_events)


class ExecutorTriggerAnalyse(Task, AnalyseTriggerMixin):
    ignore_result = True
    result_model = AlarmHistory
    name = 'executor.analysetrigger'
    sender_class = RabbitMQChannelSender

    def run(self, *args, **kwargs):
        self.data_source = kwargs

        passd = False
        error = ''
        notes = ''
        topub = True
        tqueryset_list = []
        owner = self.get_owner()
        trigger_engine = self.engine_class()
        alarmstrategy = self.get_alarmstrategy()
        strategyrules = alarmstrategy.rules
        for host in alarmstrategy.hosts.all():
            trigger_engine.rules = self.render_rules(strategyrules, host)
            try:
                passd = trigger_engine.evaluate()
            except TriggerError as e:
                error = e
                passd = True
                topub = False
            if passd is False:
                continue
            if topub is False:
                # message notice
                continue
            grade = alarmstrategy.get_grade_display()
            name = self.render_data(alarmstrategy.name, {'object': host})
            notes = self.render_data(alarmstrategy.notes, {'object': host})
            print '[{0}] trigger: {1} detail: {2} exception: {3}'.format(grade, name, notes, error)
            history = self.result_model(name=name, notes=notes, error=error, host=host, owner=owner,
                                        alarmstrategy=alarmstrategy)
            tqueryset_list.append(history)
        self.result_model.objects.bulk_create(tqueryset_list)
