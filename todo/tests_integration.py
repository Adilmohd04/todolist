from datetime import datetime, timedelta
import base64
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task, Tag


class TaskIntegrationTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = "/tasks/"

        self.auth = "testuser:password"
        self.auth_encoded = base64.b64encode(self.auth.encode("utf-8")).decode("utf-8")

        self.tag1 = Tag.objects.create(name="tag1")
        self.tag2 = Tag.objects.create(name="tag2")

    def test_create_task_success(self):

        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        data = {
            "title": "Test Task",
            "description": "Test description",
            "due_date": future_date,
            "tag_names": ["tag1", "tag2"],
            "status": "OPEN",
        }
        response = self.client.post(
            self.url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get(pk=response.data["id"])
        self.assertEqual(task.title, data["title"])
        self.assertEqual(task.description, data["description"])

        self.assertEqual(
            list(task.tags.values_list("name", flat=True)), ["tag1", "tag2"]
        )

    def test_create_task_missing_field(self):
        """Test creating a task with missing required fields"""
        data = {
            "title": "Test Task",
            "due_date": "2024-12-30",
            "tags": [self.tag1.id, self.tag2.id],
            "status": "OPEN",
        }
        response = self.client.post(
            self.url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_invalid_date(self):
        """Test creating a task with an invalid date format"""
        data = {
            "title": "Test Task",
            "description": "Test description",
            "due_date": "invalid-date",
            "tags": [self.tag1.id, self.tag2.id],
            "status": "OPEN",
        }
        response = self.client.post(
            self.url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_task_success(self):
        """Test retrieving an existing task"""
        task = Task.objects.create(
            title="Test Task",
            description="Test description",
            due_date="2024-12-30",
            status="OPEN",
        )
        task.tags.set([self.tag1, self.tag2])
        url = f"/tasks/{task.pk}/"
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_not_found(self):
        """Test retrieving a non-existent task"""
        url = "/tasks/999999/"
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_success(self):
        """Test updating an existing task"""
        task = Task.objects.create(
            title="Test Task",
            description="Test description",
            due_date="2024-12-30",
            status="OPEN",
        )
        task.tags.set([self.tag1, self.tag2])
        url = f"/tasks/{task.pk}/"
        data = {"status": "COMPLETED"}
        response = self.client.put(
            url, data, HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, "COMPLETED")

    def test_update_task_not_found(self):
        """Test updating a non-existent task"""
        url = "/tasks/999999/"
        data = {"status": "COMPLETED"}
        response = self.client.put(
            url, data, HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_invalid_data(self):
        """Test updating a task with invalid data"""
        task = Task.objects.create(
            title="Test Task",
            description="Test description",
            due_date="2024-12-30",
            status="OPEN",
        )
        task.tags.set([self.tag1, self.tag2])
        url = f"/tasks/{task.pk}/"
        data = {"status": "INVALID_STATUS"}
        response = self.client.put(
            url, data, HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_task_success(self):
        """Test deleting a task"""
        task = Task.objects.create(
            title="Test Task",
            description="Test description",
            due_date="2024-12-30",
            status="OPEN",
        )
        task.tags.set([self.tag1, self.tag2])
        url = f"/tasks/{task.pk}/"
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task"""
        url = "/tasks/999999/"
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Basic {self.auth_encoded}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authentication_failed(self):
        """Test failed authentication with invalid credentials"""
        invalid_auth = "invalid_username:invalid_password"
        invalid_auth_encoded = base64.b64encode(invalid_auth.encode("utf-8")).decode(
            "utf-8"
        )
        data = {"title": "Test Task", "description": "Test description"}
        response = self.client.post(
            self.url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Basic {invalid_auth_encoded}",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
