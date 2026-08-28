from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exam_list, name='list'),
    path('create/', views.exam_create, name='create'),
    path('<int:pk>/', views.exam_detail, name='detail'),
    path('<int:pk>/update/', views.exam_update, name='update'),
    path('<int:pk>/delete/', views.exam_delete, name='delete'),
]
