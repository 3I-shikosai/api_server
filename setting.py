wsgi_app = "app.main:app"

ch_dir = "./"

bind = "0.0.0.0:8080"

# workers = 8
workers = 8

worker_class = "uvicorn_worker.UvicornWorker"

accesslog = './access.log'
loglevel = "info"
