from __future__ import annotations

from rest_framework import mixins, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.api.v1.tasks.serializers.serializers import TaskSerializer
from src.apps.tasks.models import Task
from src.celery_tasks.tasks import process_task


class TaskViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def create(self, request: Request, *args, **kwargs) -> Response:
        response = super().create(request, *args, **kwargs)
        task_id = response.data["id"]
        process_task.delay(task_id)
        return response
