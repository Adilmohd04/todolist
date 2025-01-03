from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Task


class TaskModelTest(TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            due_date=datetime(2024, 12, 31),
            status="OPEN",
        )

    def test_task_creation(self):
        task = self.task
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.due_date.date(), datetime(2024, 12, 31).date())
        self.assertEqual(task.status, "OPEN")

    def test_timestamp_auto_set(self):
        task = self.task
        self.assertIsNotNone(task.timestamp)
        original_timestamp = task.timestamp
        task.save()
        self.assertEqual(task.timestamp, original_timestamp)

    def test_title_max_length(self):
        long_title = "a" * 101
        task = Task(title=long_title, description="Test", status="OPEN")
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_description_max_length(self):
        long_description = "a" * 1001
        task = Task(title="Test Task", description=long_description, status="OPEN")
        try:
            task.full_clean()
            self.fail("ValidationError not raised")
        except ValidationError:
            pass

    def test_empty_description(self):
        task = Task(title="Test Task", description="", status="OPEN")
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_due_date_optional(self):
        task = Task(title="Test Task", description="Test", status="OPEN")
        task.full_clean()

    def test_tag_unique(self):
        task = Task(
            title="Test Task",
            description="Test",
            tags="tag1, tag2, tag1",
            status="OPEN",
        )
        task.save()
        task = Task.objects.get(id=task.id)
        self.assertEqual(task.tags, "tag1, tag2")

    def test_status_choices(self):
        valid_statuses = [
            "OPEN",
            "WORKING",
            "PENDING_REVIEW",
            "COMPLETED",
            "OVERDUE",
            "CANCELLED",
        ]
        for status in valid_statuses:
            task = Task(title="Test Task", description="Test", status=status)
            task.full_clean()

        invalid_status = "INVALID_STATUS"
        task = Task(title="Test Task", description="Test", status=invalid_status)
        with self.assertRaises(ValidationError):
            task.full_clean()
