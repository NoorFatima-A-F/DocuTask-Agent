"""Celery application (broker: Redis). Run a worker with::

    celery -A app.jobs.celery_app worker --loglevel=info --concurrency=2

Delivery is at-least-once: tasks are acknowledged after they finish (``acks_late``) and
re-queued if the worker dies (``reject_on_worker_lost``). The task is idempotent because
the job row's status is checked before any work runs.
"""

from celery import Celery

from app.core.config import settings

#: Seconds Redis waits for an ack before redelivering a task. Must exceed the longest job.
VISIBILITY_TIMEOUT_SECONDS = 60 * 60

celery_app = Celery(
    "docutask",
    # Without REDIS_URL the API refuses to enqueue (QUEUE_UNAVAILABLE); "memory://" only serves eager tests.
    broker=settings.REDIS_URL or "memory://",
    include=["app.jobs.tasks"],
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_ignore_result=True,  # job status lives in the database
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    broker_transport_options={"visibility_timeout": VISIBILITY_TIMEOUT_SECONDS},
    broker_connection_retry_on_startup=True,
    task_default_queue="extraction",
    timezone="UTC",
)
