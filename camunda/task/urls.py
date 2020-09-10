from django.urls import path
from task.views import TasksByUserIDAPIView, Tasks, TaskInfo

urlpatterns = [
    path('tasks/', Tasks.as_view()),
    path('tasks/<int:assignee>', TasksByUserIDAPIView.as_view()),
    path('taskinfo/', TaskInfo.as_view())
]