import time
from collections import OrderedDict
from threading import Lock
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RateLimitStore:
    """
    Thread-safe in-memory rate limit store with LRU eviction.
    Max 10,000 tracked IPs to prevent memory exhaustion attacks.
    """

    MAX_IPS = 10_000

    def __init__(self):
        self._data = OrderedDict()
        self._lock = Lock()

    def _evict_expired(self, window, now):
        """Remove expired entries from oldest side."""
        while self._data:
            ip, timestamps = next(iter(self._data.items()))
            alive = [t for t in timestamps if now - t < window]
            if not alive:
                del self._data[ip]
            else:
                self._data[ip] = alive
                break

    def _ensure_capacity(self):
        """Evict oldest IPs if over capacity."""
        while len(self._data) > self.MAX_IPS:
            self._data.popitem(last=False)

    def record(self, ip, window):
        now = time.time()
        with self._lock:
            self._evict_expired(window, now)
            self._ensure_capacity()
            if ip in self._data:
                self._data[ip].append(now)
            else:
                self._data[ip] = [now]

    def count(self, ip, window):
        now = time.time()
        with self._lock:
            self._evict_expired(window, now)
            timestamps = self._data.get(ip, [])
            alive = [t for t in timestamps if now - t < window]
            if alive:
                self._data[ip] = alive
            elif ip in self._data:
                del self._data[ip]
            return len(alive)

    def remaining(self, ip, window, max_attempts):
        now = time.time()
        with self._lock:
            timestamps = self._data.get(ip, [])
            alive = [t for t in timestamps if now - t < window]
            return max(0, max_attempts - len(alive))

    def reset(self, ip):
        with self._lock:
            self._data.pop(ip, None)

    def __len__(self):
        return len(self._data)


# Global shared store
_global_store = RateLimitStore()
_login_store = RateLimitStore()


class GlobalRateLimitMiddleware(MiddlewareMixin):
    """
    Rate limits ALL incoming requests per IP.
    
    Limits:
    - Anonymous: 60 requests/min (1/sec average)
    - Authenticated: 120 requests/min
    - POST endpoints: 20 requests/min (form submissions)
    
    Returns 429 Too Many Requests when exceeded.
    Disabled when DEBUG=True (development/testing).
    """

    ANON_LIMIT = 60
    AUTH_LIMIT = 120
    POST_LIMIT = 20
    WINDOW = 60  # seconds

    def process_request(self, request):
        from django.conf import settings
        if settings.DEBUG:
            return None

        ip = self._get_client_ip(request)

        if request.method == 'POST':
            count = _global_store.count(ip, self.WINDOW)
            if count >= self.POST_LIMIT:
                return self._rate_limited()
            _global_store.record(ip, self.WINDOW)
        else:
            count = _global_store.count(ip, self.WINDOW)
            limit = self.AUTH_LIMIT if request.user.is_authenticated else self.ANON_LIMIT
            if count >= limit:
                return self._rate_limited()
            _global_store.record(ip, self.WINDOW)

    def _get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')

    def _rate_limited(self):
        response = HttpResponse(
            '<html><body><h1>429 Too Many Requests</h1>'
            '<p>Слишком много запросов. Подождите минуту.</p>'
            '</body></html>',
            status=429,
        )
        response['Retry-After'] = '60'
        response['Content-Type'] = 'text/html; charset=utf-8'
        return response


class LoginRateLimitMiddleware(MiddlewareMixin):
    """
    Specific rate limiter for login attempts.
    5 failed attempts per 15 minutes per IP.
    """

    MAX_ATTEMPTS = 5
    WINDOW = 900  # 15 minutes

    def process_request(self, request):
        ip = self._get_client_ip(request)
        if _login_store.count(ip, self.WINDOW) >= self.MAX_ATTEMPTS:
            remaining = self._get_remaining(ip)
            return HttpResponse(
                '<html><body><h1>429 Too Many Requests</h1>'
                f'<p>Слишком много попыток входа. Попробуйте через {remaining // 60} мин.</p>'
                '</body></html>',
                status=429,
            )

    def _get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')

    def _get_remaining(self, ip):
        return _login_store.remaining(ip, self.WINDOW, self.MAX_ATTEMPTS)

    @classmethod
    def record_failed(cls, ip):
        _login_store.record(ip, cls.WINDOW)

    @classmethod
    def reset(cls, ip):
        _login_store.reset(ip)

    @classmethod
    def is_rate_limited(cls, ip):
        return _login_store.count(ip, cls.WINDOW) >= cls.MAX_ATTEMPTS

    @classmethod
    def get_remaining_time(cls, ip):
        return _login_store.remaining(ip, cls.WINDOW, cls.MAX_ATTEMPTS)


class RequestTimeoutMiddleware(MiddlewareMixin):
    """
    Adds X-Request-Timeout headers and tracks slow requests.
    Does NOT enforce timeouts (that's Gunicorn/Nginx's job),
    but signals the reverse proxy.
    """

    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            response['X-Request-Duration'] = f'{duration:.3f}s'
            if duration > 5:
                import logging
                logger = logging.getLogger('django.security')
                logger.warning(
                    'Slow request: %s %s took %.2fs',
                    request.method, request.path, duration,
                )
        return response


# Keep backward-compatible alias
RateLimitMiddleware = LoginRateLimitMiddleware
