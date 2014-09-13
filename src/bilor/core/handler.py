import datetime
import logging
import sys
import traceback

import requests
from werkzeug.debug.tbtools import get_current_traceback
from django.utils.encoding import force_text


class BilorHandler(logging.Handler):
    """Logging handler for bilor.

    Based on the raven logging handler.
    """

    def __init__(self, endpoint, *args, **kwargs):
        super(BilorHandler, self).__init__(level=kwargs.get('level', logging.NOTSET))
        self.endpoint = endpoint

    def can_record(self, record):
        return not (
            record.name == 'bilor' or
            record.name.startswith('bilor.')
        )

    def emit(self, record):
        try:
            self.format(record)

            if not self.can_record(record):
                print(force_text(record.message), file=sys.stderr)
                return

            return self._emit(record)
        except Exception:
            print("Top level Bilor exception caught - failed creating log record", file=sys.stderr)
            print(force_text(record.msg), file=sys.stderr)
            print(force_text(traceback.format_exc()), file=sys.stderr)

    def _emit(self, record, **kwargs):
        data = {}

        extra = getattr(record, 'data', None)
        if not isinstance(extra, dict):
            if extra:
                extra = {'data': extra}
            else:
                extra = {}

        date = datetime.datetime.utcfromtimestamp(record.created)
        data = {
            'params': record.args,
        }
        try:
            data['message'] = force_text(record.msg)
        except UnicodeDecodeError:
            # Handle binary strings where it should be unicode...
            data['message'] = repr(record.msg)[1:-1]

        try:
            data['formatted'] = force_text(record.message)
        except UnicodeDecodeError:
            # Handle binary strings where it should be unicode...
            data['formatted'] = repr(record.message)[1:-1]

        # If there's no exception being processed, exc_info may be a 3-tuple of None
        # http://docs.python.org/library/sys.html#sys.exc_info
        if record.exc_info and all(record.exc_info):
            data['traceback'] = get_current_traceback(skip=1)


        data['level'] = record.levelno
        data['logger'] = record.name

        if hasattr(record, 'tags'):
            data['tags'] = record.tags
