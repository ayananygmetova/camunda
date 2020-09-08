from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models import Task
from task.serializers import TaskSerializer


class Tasks(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name')

class TasksByUserIDAPIView(APIView):
    def get(self, request, user_id):
        task = Task.objects.filter(user_id=user_id)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)