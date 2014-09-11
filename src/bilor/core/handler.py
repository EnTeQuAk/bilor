import datetime
import logging
import sys
import traceback

import requests

from werkzeug.debug.tbtools import get_current_traceback


class BilorHandler(logging.Handler):
    """Logging handler for bilor.

    Based on raven.
    """

    def __init__(self, host, *args, **kwargs):
        super(BilorHandler, self).__init__(level=kwargs.get('level', logging.NOTSET))
        self.host = host

    def can_record(self, record):
        return not (
            record.name == 'bilor' or
            record.name.startswith('bilor.')
        )

    def emit(self, record):
        try:
            self.format(record)

            if not self.can_record(record):
                print(to_string(record.message), file=sys.stderr)
                return

            return self._emit(record)
        except Exception:
            if self.client.raise_send_errors:
                raise
            print("Top level Bilor exception caught - failed creating log record", file=sys.stderr)
            print(to_string(record.msg), file=sys.stderr)
            print(to_string(traceback.format_exc()), file=sys.stderr)

    def _emit(self, record, **kwargs):
        data = {}

        extra = getattr(record, 'data', None)
        if not isinstance(extra, dict):
            if extra:
                extra = {'data': extra}
            else:
                extra = {}

        stack = getattr(record, 'stack', None)
        if stack is True:
            stack = get_current_traceback(skip=1)

        date = datetime.datetime.utcfromtimestamp(record.created)
        handler_kwargs = {
            'params': record.args,
        }
        try:
            handler_kwargs['message'] = six.text_type(record.msg)
        except UnicodeDecodeError:
            # Handle binary strings where it should be unicode...
            handler_kwargs['message'] = repr(record.msg)[1:-1]

        try:
            handler_kwargs['formatted'] = six.text_type(record.message)
        except UnicodeDecodeError:
            # Handle binary strings where it should be unicode...
            handler_kwargs['formatted'] = repr(record.message)[1:-1]

        # If there's no exception being processed, exc_info may be a 3-tuple of None
        # http://docs.python.org/library/sys.html#sys.exc_info
        if record.exc_info and all(record.exc_info):
            # capture the standard message first so that we ensure
            # the event is recorded as an exception, in addition to having our
            # message interface attached
            handler = self.client.get_handler(event_type)
            data.update(handler.capture(**handler_kwargs))

            handler_kwargs = {'exc_info': record.exc_info}

        data['level'] = record.levelno
        data['logger'] = record.name

        if hasattr(record, 'tags'):
            kwargs['tags'] = record.tags

        kwargs.update(handler_kwargs)

        #requests.post()
