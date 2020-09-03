from django.shortcuts import render
from rest_framework import generics, filters

from .models import Tasks
from .serializers import TaskSerializer

class TaskView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Tasks.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['process_variable', 'name']