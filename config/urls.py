"""config URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', set_language, name='set_language'),
    path('', include('apps.dashboard.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('semesters/', include('apps.semesters.urls')),
    path('subjects/', include('apps.subjects.urls')),
    path('schedule/', include('apps.schedule.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('grades/', include('apps.grades.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('exams/', include('apps.exams.urls')),
    path('calendar/', include('apps.calendar.urls')),
    path('notes/', include('apps.notes.urls')),
    path('goals/', include('apps.goals.urls')),
    path('productivity/', include('apps.productivity.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('core/', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
