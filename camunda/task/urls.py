from django.urls import path
from task.views import TasksByUserIDAPIView, Tasks

urlpatterns = [
    path('tasks/', Tasks.as_view()),
    path('tasks/<int:user_id>', TasksByUserIDAPIView.as_view())
]