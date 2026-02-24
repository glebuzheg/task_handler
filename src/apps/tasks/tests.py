from __future__ import annotations

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from src.apps.tasks.enums import Status
from src.apps.tasks.models import Task
from src.apps.tasks.services.services import TaskService


class TaskAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_task_sets_status_new_and_enqueues(self) -> None:
        response = self.client.post(
            reverse("task-list"),
            {"title": "Process report"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        task = Task.objects.get(id=response.data["id"])
        self.assertEqual(task.status, Status.NEW)

    def test_service_changes_status_and_result_even_length(self) -> None:
        task = Task.objects.create(title="even")  # len=4
        TaskService.start_processing(task)
        TaskService.complete_processing(task)
        task.save()
        task.refresh_from_db()
        self.assertEqual(task.status, Status.DONE)
        self.assertEqual(task.result, "success")

    def test_service_changes_status_and_result_odd_length(self) -> None:
        task = Task.objects.create(title="odd")  # len=3
        TaskService.start_processing(task)
        TaskService.complete_processing(task)
        task.save()
        task.refresh_from_db()
        self.assertEqual(task.status, Status.FAILED)
        self.assertEqual(task.result, "error")

    def test_filtering_by_status(self) -> None:
        Task.objects.create(title="t1", status=Status.NEW)
        Task.objects.create(title="t2", status=Status.DONE)

        response = self.client.get(reverse("task-list"), {"status": Status.NEW})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(item["status"] == Status.NEW for item in response.data["results"]))
