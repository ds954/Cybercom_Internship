from celery import shared_task
from time import sleep

@shared_task
def sleep_well(duration):
    print('sleeping for {0} sec'.format(duration))
    sleep(duration)