release: flask db upgrade
web: gunicorn --access-logfile '-' --workers 2 manage:app --log-file - --log-level debug
worker: celery worker -A celery_worker.celery_app --loglevel=info --concurrency=4