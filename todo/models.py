from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from datetime import datetime


class Task(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("WORKING", "Working"),
        ("PENDING_REVIEW", "Pending Review"),
        ("COMPLETED", "Completed"),
        ("OVERDUE", "Overdue"),
        ("CANCELLED", "Cancelled"),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=100)

    description = models.TextField(max_length=1000)

    due_date = models.DateField(null=True, blank=True)

    tags = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    def save(self, *args, **kwargs):
        if self.tags:
            tags_list = [tag.strip() for tag in self.tags.split(",")]
            unique_tags = ", ".join(sorted(set(tags_list)))
            self.tags = unique_tags
        super().save(*args, **kwargs)

    def clean(self):
        if self.due_date and self.due_date < now().date():
            raise ValidationError({"due_date": "Due date cannot be in the past."})
        try:
            if self.due_date:
                datetime.strptime(str(self.due_date), "%Y-%m-%d")
        except ValueError:
            raise ValidationError({"due_date": "Invalid date format. Use YYYY-MM-DD."})

        if len(self.description) > 1000:
            raise ValidationError(
                {"description": "Description cannot exceed 1000 characters."}
            )

    def __str__(self):
        return self.title
