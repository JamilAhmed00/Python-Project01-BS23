
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Task
from .serializers import UserSerializer, TaskSerializer


class IsAdminOrAssignedUser(permissions.BasePermission):

    

    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
            return True

        if view.action in ['retrieve', 'list']:
            return obj.assigned_to == request.user

        if view.action in ['update', 'partial_update']:
            return obj.assigned_to == request.user

        return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrAssignedUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()

        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)
