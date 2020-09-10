from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import json
import random
from task.models import Task
from task.serializers import TaskSerializer
# from rest_framework.permissions import IsAuthenticated


class Tasks(generics.ListCreateAPIView):
    # queryset = Task.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        serializer_class = TaskSerializer
        serializer_class.is_valid()
        serializer_class.save()
        # permission_classes = (IsAuthenticated,)
        url = 'http://dev.cheesenology.kz:8080/engine-rest/task'
        # assignee, name = (str(self.request.data.get('fio'))+" ").split(" ", 1)
        json = {
            "profile": {
                "id": int(self.request.data.get('id')),
                "name": str(self.request.data.get('name')),
                "assignee": int(self.request.data.get('assignee')),
                "process_id": str(self.request.data.get('process_id'))
                # "credentials": {
                #     "password": self.request.data.get('password')
                # }
            }
        }
        requests.post(url, json=json)
        return Response(serializer_class.data,
                        status=status.HTTP_200_OK)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)
        serializer_class = TaskSerializer(data={"id": self.request.data.get('id'),
                                                "name": self.request.data.get('name'),
                                                "assignee": self.request.data.get('assignee'),
                                                "process_id": self.request.data.get('process_id')})
        serializer_class.is_valid()
        serializer_class.save()
        url = 'http://dev.cheesenology.kz:8080/engine-rest/task'
        json = {"taskVariables":
                    [{"name": self.request.data.get('name'),
                    "value": "varValue",
                    "operator": "eq"
                    },
                    {"name": self.request.data.get('name'),
                    "value": 30,
                    "operator": "neq"}],
                    "processInstanceBusinessKeyIn": "aBusinessKey,anotherBusinessKey",
                    "assigneeIn": self.request.data.get('assignee'),
                    "priority":10,
                    "sorting":
                    [{"sortBy": "dueDate",
                    "sortOrder": "asc"
                    },
                    {"sortBy": "processVariable",
                    "sortOrder": "desc",
                    "parameters": {
                      "variable": "orderId",
                      "type": "String"
                    }}]
                }
        # surname, name = (str(self.request.data.get('fio')) + " ").split(" ", 1)
        # json = {
        #     "profile": {
        #         "id": str(self.request.data.get('id')),
        #         "name": str(self.request.data.get('name')),
        #         "assignee": int(self.request.data.get('assignee')),
        #         "process_id": str(self.request.data.get('process_id'))
        #         # "credentials": {
        #         #     "password": self.request.data.get('password')
        #         # }
        #     }
        # }
        requests.post(url, json=json)
        return Response(serializer_class.data,
                        status=status.HTTP_200_OK)

class TasksByUserIDAPIView(APIView):
    def get(self, request, assignee):
        task = Task.objects.filter(assignee=assignee)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

class TaskInfo(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = self.request.user
        url = 'http://dev.cheesenology.kz:8080/engine-rest/task?assignee='+str(user.camunda_id)
        requests.post(url)
        return Response(request.text)

