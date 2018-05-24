#! -*- coding: utf-8 -*-


from .enhance import Switch
from datetime import datetime, timedelta


def get_last_day_range():
    now = datetime.now()
    last_day = now - timedelta(days=1)

    _from = datetime(last_day.year, last_day.month, last_day.day, 0, 0)
    _until = datetime(last_day.year, last_day.month, last_day.day, 23, 59)

    return _from, _until


def get_last_week_range():
    now = datetime.now()
    last_week_from = now - timedelta(days=now.weekday()+7)
    last_week_until = now - timedelta(days=now.weekday()+1)

    _from = datetime(last_week_from.year, last_week_from.month, last_week_from.day, 0, 0)
    _until = datetime(last_week_until.year, last_week_until.month, last_week_until.day, 23, 59)

    return _from, _until


def get_last_quarter_range():
    now = datetime.now()
    curr_quarter_from = datetime(now.year, now.month, 1, 23, 59)

    _from = datetime(now.year, now.month - 3, 1, 0, 0)
    _until = curr_quarter_from - timedelta(days=1)

    return _from, _until


def get_last_year_range():
    now = datetime.now()
    curr_year_from = datetime(now.year, 1, 1, 0, 0)
    curr_quarter_until = datetime(now.year+1, 1, 1, 23, 59) - timedelta(days=1)

    _from = curr_year_from - timedelta(days=1)
    _until = curr_quarter_until - timedelta(days=1)

    return _from, _until


def get_date_range(name='last_day', fmt='%H:%M_%Y%m%d'):
    for case in Switch(name):
        if case('last_day'):
            _from, _until = get_last_day_range()
            break
        if case('last_week'):
            _from, _until = get_last_week_range()
            break
        if case('last_quarter'):
            _from, _until = get_last_quarter_range()
            break
        if case('last_year'):
            _from, _until = get_last_year_range()
            break
        if case():
            _from, _until = get_last_day_range()
            break

    return _from.strftime(fmt), _until.strftime(fmt)


def sort_metric_data(data, reverse=False):
    ziped_data = zip(data['raw_data']['labels'], data['raw_data']['avges'])
    ziped_data.pop(0)

    return sorted(ziped_data, key=lambda r: r[1], reverse=reverse)
