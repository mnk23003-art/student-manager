import os
import multiprocessing

# Server socket
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gthread'
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
worker_connections = 1000

# Timeout (seconds) — kill workers after this
timeout = 30

# Graceful timeout
graceful_timeout = 30

# Keep-alive
keepalive = 5

# Max requests per worker (restarts worker after N requests to prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Security
limit_request_line = 4094  # Max bytes in request line (URL)
limit_request_fields = 100  # Max number of request headers
limit_request_field_size = 8190  # Max bytes per request header

# Logging
accesslog = os.environ.get('GUNICORN_ACCESS_LOG', 'logs/access.log')
errorlog = os.environ.get('GUNICORN_ERROR_LOG', 'logs/error.log')
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'warning')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'student_manager'

# Server mechanics
preload_app = True
daemon = False

# SSL (uncomment for direct SSL, recommended to use Nginx instead)
# certfile = '/etc/ssl/certs/server.crt'
# keyfile = '/etc/ssl/private/server.key'
