from django.contrib import admin
from .models import Task, Tag

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "due_date", "timestamp")
    list_filter = ("status", "due_date", "timestamp")
    search_fields = ("title", "description", "tags")
    list_per_page = 5
    ordering = ("-timestamp",)
    list_editable = ("status",)
    readonly_fields = ("timestamp",)
    fieldsets = (
        ("Basic Information", {"fields": ("title", "description", "status")}),
        ("Additional Details", {"fields": ("tags", "due_date", "timestamp")}),
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
