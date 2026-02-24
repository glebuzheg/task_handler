from __future__ import annotations

from src.apps.tasks.enums import Status
from src.apps.tasks.models import Task


class TaskService:
    @staticmethod
    def start_processing(task: Task) -> None:
        task.status = Status.PROCESSING

    @staticmethod
    def complete_processing(task: Task) -> None:
        title_length = len(task.title or "")
        if title_length % 2 == 0:
            task.status = Status.DONE
            task.result = "success"
        else:
            task.status = Status.FAILED
            task.result = "error"

