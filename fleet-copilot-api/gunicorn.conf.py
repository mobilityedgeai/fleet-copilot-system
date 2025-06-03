import os

bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = 2
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
accesslog = "-"
errorlog = "-"
loglevel = "info"

