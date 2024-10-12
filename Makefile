.PHONY: format run uvicorn setup
format:
	poetry run black ./


run:
	rm userdata.db
	poetry run gunicorn --config ./setting.py


uvicorn:
	rm userdata.db
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload


setup:
	poetry install
