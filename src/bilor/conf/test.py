import uuid
from bilor.conf.base import *


ELASTICSEARCH_CONNECTION = {
    'hosts': ['localhost'],
    'index_name': uuid.uuid4().hex,
    'sniff_on_start': True,
    'sniff_on_connection_fail': True,
    'sniffer_timeout': 60
}
