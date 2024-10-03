wsgi_app = 'main:app'

ch_dir = './'

bind = '0.0.0.0:8080'

workers = 4

worker_class = 'uvicorn_worker.UvicornWorker'

# accesslog = './access.log'
accesslog = '-'
loglevel = 'info'
