from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('search/', views.global_search, name='search'),
    path('export/', views.export_view, name='export_data'),
    path('import/', views.import_view, name='import_view'),
    path('backups/', views.backup_list, name='backup_list'),
    path('backups/create/', views.backup_create, name='backup_create'),
    path('backups/<str:filename>/restore/', views.backup_restore, name='backup_restore'),
    path('backups/<str:filename>/delete/', views.backup_delete, name='backup_delete'),
]
