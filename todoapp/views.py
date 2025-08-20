from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Task
from .serializers import UserSerializer, TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:  
            return True
        if view.action in ['list', 'retrieve']:
            return True
        return False

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.assigned_to == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow signup

   




class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:  
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise permissions.PermissionDenied("Only admin can create tasks.")
