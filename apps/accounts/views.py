from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.urls import reverse_lazy, resolve
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from apps.core.rate_limit import RateLimitMiddleware
from .forms import (
    UserRegistrationForm, UserLoginForm, UserUpdateForm,
    ProfileUpdateForm, UserSettingsForm, CustomPasswordChangeForm
)
from .models import StudentProfile, UserSettings


def _is_safe_url(url):
    """Check if redirect URL is safe (same host, no protocol)."""
    if not url:
        return False
    # Only allow relative URLs starting with /
    if not url.startswith('/') or url.startswith('//'):
        return False
    # No protocol in URL
    if '://' in url:
        return False
    return True


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            UserSettings.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Welcome to Student Manager!')
            return redirect('accounts:onboarding')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        ip = self._get_client_ip(request)
        
        if RateLimitMiddleware.is_rate_limited(ip):
            remaining = RateLimitMiddleware.get_remaining_time(request)
            messages.error(request, f'Sлишком много попыток. Попробуйте через {remaining // 60} мин.')
            return render(request, 'accounts/login.html', {'form': UserLoginForm()})
        
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            RateLimitMiddleware.clear_attempts(ip)
            login(request, user)
            next_url = request.GET.get('next', '')
            if _is_safe_url(next_url):
                return redirect(next_url)
            return redirect('dashboard:index')
        else:
            RateLimitMiddleware.record_failed_attempt(ip)
        return render(request, 'accounts/login.html', {'form': form})
    
    def _get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    user = request.user
    profile, _ = StudentProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    })


@login_required
def settings_view(request):
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated!')
            return redirect('accounts:settings')
    else:
        form = UserSettingsForm(instance=user_settings)
    
    return render(request, 'accounts/settings.html', {'form': form, 'user_settings': user_settings})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Invalidate all other sessions for this user
        from django.contrib.sessions.models import Session
        from django.utils import timezone
        user = self.request.user
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            data = session.get_decoded()
            if data.get('_auth_user_id') == str(user.pk):
                if session.session_key != self.request.session.session_key:
                    session.delete()
        messages.success(self.request, 'Пароль изменён. Все другие сессии деактивированы.')
        return response


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:login')


@login_required
def onboarding_view(request):
    try:
        step = int(request.GET.get('step', 1))
    except (ValueError, TypeError):
        step = 1
    step = max(1, min(step, 6))
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if step == 2:
            profile.university = request.POST.get('university', '')
            profile.faculty = request.POST.get('faculty', '')
            profile.specialization = request.POST.get('specialization', '')
            profile.course = request.POST.get('course') or None
            profile.academic_year = request.POST.get('academic_year', '')
            profile.save()
        
        if step < 6:
            return redirect(f'/accounts/onboarding/?step={step + 1}')
        else:
            return redirect('dashboard:index')
    
    return render(request, 'accounts/onboarding.html', {'step': step, 'profile': profile})


@login_required
def set_language_view(request, lang):
    if lang in ('en', 'ru'):
        user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
        user_settings.language = lang
        user_settings.save()
        request.session['django_language'] = lang
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:index'))


@login_required
def set_theme_view(request, theme):
    if theme in ('light', 'dark', 'system'):
        user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
        user_settings.theme = theme
        user_settings.save()
    referer = request.META.get('HTTP_REFERER', 'dashboard:index')
    return redirect(referer)
