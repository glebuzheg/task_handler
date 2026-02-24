from __future__ import annotations

import time

from celery import shared_task
from django.db import transaction

from src.apps.tasks.models import Task
from src.apps.tasks.services.services import TaskService


@shared_task
def process_task(task_id: int) -> None:
    with transaction.atomic():
        task = Task.objects.select_for_update().get(id=task_id)
        TaskService.start_processing(task)
        task.save(update_fields=["status", "updated_at"])

    time.sleep(3)

    with transaction.atomic():
        task = Task.objects.select_for_update().get(id=task_id)
        TaskService.complete_processing(task)
        task.save(update_fields=["status", "result", "updated_at"])

