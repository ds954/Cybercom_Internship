import os
from celery.schedules import crontab
from celery import Celery
from time import sleep

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myceleryproject.settings')

app = Celery('myceleryproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY') 

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(name='addition')
def add(x,y):
    sleep(5)
    return x+y

app.conf.beat_schedule={
    'every-10-second':{
        'task':'myapp.tasks.clear_session_cashe',
        # 'schedule':10,
        'schedule':crontab(minute='*/1'),

        'args':('1111',)

    }

}