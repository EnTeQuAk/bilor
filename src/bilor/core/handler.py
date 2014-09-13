import json
import logging
import sys
import traceback

import requests
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from werkzeug.debug.tbtools import get_current_traceback
from werkzeug.utils import escape


class BilorHandler(logging.Handler):
    """Logging handler for bilor.

    Based on the raven logging handler.
    """
    def __init__(self, host, *args, **kwargs):
        assert host.startswith('http')
        super(BilorHandler, self).__init__(level=kwargs.get('level', logging.NOTSET))
        self.host = host.rstrip('/')

    def emit(self, record):
        try:
            self.format(record)
            return self._emit(record)
        except Exception:
            print(
                'Top level Bilor exception caught - failed creating log record',
                file=sys.stderr)
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

        data = {
            'params': record.args,
            'created': record.created
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
            tb = get_current_traceback(skip=1)
            exc = escape(tb.exception)
            serialized_frames = []
            for frame in tb.frames:
                serialized_frame = {
                    'id': frame.id,
                    'filename': escape(frame.filename),
                    'lineno': frame.lineno,
                    'function_name': escape(frame.function_name),
                    'current_line': escape(frame.current_line.strip()),
                    'sourcelines': frame.sourcelines,
                    'lines': []
                }

                for line in frame.get_annotated_lines():
                    serialized_frame['lines'].append({
                        'classes': line.classes,
                        'lineno': line.lineno,
                        'code': escape(line.code)
                    })

                serialized_frames.append(serialized_frame)

            data['traceback'] = {
                'title': exc,
                'exception': exc,
                'exception_type': escape(tb.exception_type),
                'frames': serialized_frames,
                'plaintext': tb.plaintext,
                'traceback_id': tb.id,
            }

        data['level'] = record.levelno
        data['logger'] = record.name

        if hasattr(record, 'tags'):
            data['tags'] = record.tags

        endpoint = self.host + reverse('api-v1:message')
        headers = {'content-type': 'application/json'}
        requests.post(endpoint, data=json.dumps(data), headers=headers)
