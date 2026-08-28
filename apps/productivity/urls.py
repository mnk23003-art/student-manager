from django.urls import path
from . import views

app_name = 'productivity'

urlpatterns = [
    path('', views.productivity_view, name='view'),
    path('start/', views.start_focus_session, name='start_session'),
    path('<int:pk>/stop/', views.stop_focus_session, name='stop_session'),
    path('settings/', views.pomodoro_settings, name='settings'),
]
