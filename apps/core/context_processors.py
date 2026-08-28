def global_context(request):
    context = {
        'active_semester': getattr(request, 'active_semester', None),
        'unread_notifications': 0,
    }
    if request.user.is_authenticated:
        from apps.notifications.models import Notification
        context['unread_notifications'] = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
        from apps.accounts.models import UserSettings
        user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
        context['user_settings'] = user_settings
        if not request.session.get('django_language'):
            request.session['django_language'] = user_settings.language
    return context
