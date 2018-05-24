#! -*- coding: utf-8 -*-


from celery.task import task


@task(bind=True, max_retries=3)
def monitoring_overview_dispatcher(self, **kwargs):
    task_id = self.request.id

    return task_id


@task(bind=True, max_retries=3)
def monitoring_detailed_dispatcher(self, **kwargs):
    task_id = self.request.id

    return task_id


@task(bind=True, max_retries=3)
def codedeploy_overview_dispatcher(self, **kwargs):
    task_id = self.request.id

    return task_id


@task(bind=True, max_retries=3)
def resources_occupy_low_dispatcher(self, **kwargs):
    task_id = self.request.id

    return task_id


@task(bind=True, max_retries=3)
def resources_occupy_high_dispatcher(self, **kwargs):
    task_id = self.request.id

    return task_id
