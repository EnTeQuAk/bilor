import time
import logging
from bilor.core.handler import BilorHandler

logger = logging.getLogger('other.example')
logger.addHandler(BilorHandler('http://localhost:8000/'))


def full():
    logger.debug('This is debug')
    logger.warning('This is warning')
    logger.info('This is info')
    logger.error('This is error')


    try:
        1 / 0
    except Exception:
        logger.exception('This occurred')

print('Initial test')

full()

time.sleep(60)

print('Successful throttling test')
for idx in range(12):
    full()

time.sleep(60)

print('Expected to run into throttling')
for idx in range(24):
    full()

