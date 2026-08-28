from django.urls import path
from . import views

app_name = 'calendar'

urlpatterns = [
    path('', views.calendar_view, name='view'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:pk>/update/', views.event_update, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
]
