

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=False),
        required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'task_name', 'details', 'start_date', 'end_date', 'assigned_to', 'is_completed']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if not user.is_staff:
            if 'is_completed' in validated_data:
                instance.is_completed = validated_data['is_completed']
                instance.save()
            return instance

        return super().update(instance, validated_data)
