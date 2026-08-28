import time
from collections import defaultdict
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    """
    Simple in-memory rate limiter for login attempts.
    Tracks failed login attempts per IP address.
    """
    
    # Store: {ip: [timestamp, timestamp, ...]}
    _login_attempts = defaultdict(list)
    
    MAX_ATTEMPTS = 5
    WINDOW_SECONDS = 900  # 15 minutes
    
    @classmethod
    def _cleanup(cls, ip):
        """Remove expired entries."""
        now = time.time()
        cls._login_attempts[ip] = [
            t for t in cls._login_attempts[ip]
            if now - t < cls.WINDOW_SECONDS
        ]
        if not cls._login_attempts[ip]:
            del cls._login_attempts[ip]
    
    @classmethod
    def record_failed_attempt(cls, ip):
        """Record a failed login attempt."""
        cls._login_attempts[ip].append(time.time())
    
    @classmethod
    def clear_attempts(cls, ip):
        """Clear attempts after successful login."""
        cls._login_attempts.pop(ip, None)
    
    @classmethod
    def is_rate_limited(cls, ip):
        """Check if IP is rate limited."""
        cls._cleanup(ip)
        return len(cls._login_attempts.get(ip, [])) >= cls.MAX_ATTEMPTS
    
    @classmethod
    def get_remaining_time(cls, ip):
        """Get seconds until rate limit expires."""
        cls._cleanup(ip)
        attempts = cls._login_attempts.get(ip, [])
        if not attempts:
            return 0
        oldest = min(attempts)
        remaining = cls.WINDOW_SECONDS - (time.time() - oldest)
        return max(0, int(remaining))
