from django.urls import path
from . import views

app_name = 'semesters'

urlpatterns = [
    path('', views.semester_list, name='list'),
    path('create/', views.semester_create, name='create'),
    path('<int:pk>/update/', views.semester_update, name='update'),
    path('<int:pk>/delete/', views.semester_delete, name='delete'),
    path('<int:pk>/set-active/', views.semester_set_active, name='set_active'),
]
