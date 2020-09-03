from django.urls import path

from auth_ import views

login = views.LoginView.as_view({
    'post': 'login'})


urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', login, name='login'),
    path('change_password/', views.ChangePassword.as_view()),
    path('change_details/', views.ChangeDetails.as_view())
]
