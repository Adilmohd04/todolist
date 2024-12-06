from django.urls import path
from . import views
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    path('', views.index,name="index"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),

]
