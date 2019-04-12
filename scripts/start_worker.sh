# venv/bin/activate
# export PYTHONPATH=app/
cd app
celery worker -A celery_queue.workers