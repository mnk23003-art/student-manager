from django.core.exceptions import PermissionDenied


class UserOwnershipMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if hasattr(response, 'context_data') and response.context_data:
            obj = response.context_data.get('object')
            if obj and hasattr(obj, 'user') and obj.user != request.user:
                raise PermissionDenied
        return response
