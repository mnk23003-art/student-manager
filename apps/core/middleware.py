from django.utils.deprecation import MiddlewareMixin
from apps.semesters.models import Semester


class SemesterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            active_semester = Semester.objects.filter(
                user=request.user, is_active=True
            ).first()
            request.active_semester = active_semester
        else:
            request.active_semester = None
