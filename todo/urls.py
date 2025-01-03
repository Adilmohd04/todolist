from django.urls import path
from . import views
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    path("", views.index, name="index"),
    path("form/", views.task_form, name="task-form"),
    path("form/<int:pk>/", views.task_form, name="task-edit"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/delete/", views.task_delete, name="task-delete"
    ),  # Added delete path
]
