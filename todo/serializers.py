from rest_framework import serializers
from .models import Task
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50), required=False
    )

    class Meta:
        model = Task
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["tags"] = (
            [tag.strip() for tag in instance.tags.split(",")] if instance.tags else []
        )
        return representation

    def validate_tags(self, value):
        return list(set(value))

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        validated_data["tags"] = ",".join(tags)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags = ",".join(tags)
        return super().update(instance, validated_data)

    def validate_due_date(self, value):
        if value and value < now().date():
            raise ValidationError("Due date cannot be in the past.")
        return value
