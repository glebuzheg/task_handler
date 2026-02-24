from django.db import models


class Status(models.TextChoices):
    NEW = "new", "New"
    PROCESSING = "processing", "Processing"
    DONE = "done", "Done"
    FAILED = "failed", "Failed"
