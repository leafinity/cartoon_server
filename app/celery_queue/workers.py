import time
import os
from celery import Celery
from models.cartoon import CartoonTransformer, Style


celery = Celery('tasks')
celery.config_from_object('celery_queue.config')


@celery.task
def transform_photo(extension, image, style):
    return CartoonTransformer().transform(extension, image, Style[style.upper()])


@celery.task
def test_celery(a, b):
    # time.sleep(3)
    return 'hello world, %d' % (a + b)