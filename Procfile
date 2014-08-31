web: env PYTHONUNBUFFERED=true python manage.py runserver
worker: env PYTHONUNBUFFERED=true celery worker -A bilor.core -l INFO -E
compass: compass watch --trace
