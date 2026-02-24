from rest_framework import serializers

from src.apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status", "result", "created_at", "updated_at"]
        read_only_fields = ["id", "status", "result", "created_at", "updated_at"]
