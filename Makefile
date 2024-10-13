.PHONY: format test run build
format:
	poetry run black ./


test:
	poetry run gunicorn --config ./setting.py


run:
	podman run -p 8080:8080 fastapi


build:
	podman build -t fastapi . --no-cache=true
