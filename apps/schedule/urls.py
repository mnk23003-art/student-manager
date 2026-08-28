from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.schedule_view, name='view'),
    path('create/', views.schedule_item_create, name='create'),
    path('<int:pk>/update/', views.schedule_item_update, name='update'),
    path('<int:pk>/delete/', views.schedule_item_delete, name='delete'),
    path('conflicts/', views.schedule_check_conflicts, name='conflicts'),
]
