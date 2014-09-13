import logging
from bilor.core.handler import BilorHandler

logger = logging.getLogger('other.example')
logger.addHandler(BilorHandler('localhost'))

logger.debug('This is debug')
logger.warning('This is warning')
logger.info('This is info')
logger.error('This is error')


try:
    1 / 0
except Exception:
    logger.exception('This occurred')
