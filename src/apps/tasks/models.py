from __future__ import annotations

from django.db import models

from src.apps.tasks.enums import Status


class Task(models.Model):
    title = models.CharField("Название", max_length=255)
    status = models.CharField(
        "Статус",
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    result = models.TextField("Результат", null=True, blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        indexes = [
            models.Index(fields=["status"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Task(id={self.id}, title={self.title!r}, status={self.status})"
