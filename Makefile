all:
	@echo "Makefile"

install:
	pip install -r requirements.txt

dev:
	PYTHONPATH=src python3 -m flask --app app run
