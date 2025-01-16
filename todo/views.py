from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .models import Tag, Task
from .serializers import TaskSerializer
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator


def index(request):
    task_list = Task.objects.all().order_by("-timestamp")
    paginator = Paginator(task_list, 5)
    page_number = request.GET.get("page")
    tasks = paginator.get_page(page_number)
    context = {"tasks": tasks}
    return render(request, "todo.html", context)


def task_form(request, pk=None):
    task = None
    if pk:
        task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = parse_date(request.POST.get("due_date"))
        tags_input = request.POST.get("tags")
        status = request.POST.get("status")

        if task:
            task.title = title
            task.description = description
            task.due_date = due_date
            task.status = status
            task.save()
            task.tags.clear()
        else:
            task = Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                status=status,
            )

        # Process and add tags
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                task.tags.add(tag)

        return HttpResponseRedirect(reverse("index"))

    status_choices = Task.STATUS_CHOICES
    return render(
        request,
        "form.html",
        {
            "form_title": "Edit Task" if pk else "New Task",
            "form_action": (
                reverse("task-edit", args=[pk]) if pk else reverse("task-form")
            ),
            "task": task,
            "status_choices": status_choices,
        },
    )


def task_delete(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.delete()
        return redirect("/")
    except Task.DoesNotExist:
        return redirect("/")


class TaskListCreateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(
                {"message": "Task deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )
