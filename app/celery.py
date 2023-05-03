from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
app = Celery("car_dealer")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "buy_cars_from_provider_to_showroom": {
        "task": "core.tasks.buy_cars_from_provider_to_showroom",
        "schedule": crontab(minute="*/10"),
    },
    "buy_cars_from_showroom_to_customer": {
        "task": "core.tasks.buy_cars_from_showroom_to_customer",
        "schedule": crontab(minute="*/10"),
    },
    "check_passed_discounts": {
        "task": "core.tasks.check_passed_discounts",
        "schedule": crontab(hour="*/5"),
    },
}
