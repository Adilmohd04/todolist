from rest_framework import serializers
from .models import Task, Tag
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True, required=False
    )

    class Meta:
        model = Task
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Ensure tags are represented by their names
        representation["tags"] = [tag.name for tag in instance.tags.all()] if instance.tags.exists() else []
        return representation

    def validate_tags(self, value):
        # Ensure tags are unique
        return list(set(value))

    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        task = Task.objects.create(**validated_data)
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            task.tags.add(tag)
        return task

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        instance = super().update(instance, validated_data)
        if tag_names:
            instance.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
        return instance

    def validate_due_date(self, value):
        if value and value < now().date():
            raise ValidationError("Due date cannot be in the past.")
        return value
