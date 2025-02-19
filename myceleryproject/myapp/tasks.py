from celery import shared_task
from time import sleep

@shared_task
def sub(x, y):
    """Subtracts y from x after a 10-second delay."""
    sleep(10)
    return x - y

@shared_task
def clear_session_cache(id):
    """Clears the session cache for a given ID."""
    print(f'session cache cleared: {id}')
    return id

@shared_task
def clear_redis_data(key):
    """Clears Redis data for a given key."""
    print(f'redis data cleared: {key}')
    return key