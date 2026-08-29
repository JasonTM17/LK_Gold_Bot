.PHONY: install install-dev run check test compile lint clean

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install --upgrade pip
	python -m pip install -r requirements-dev.txt

run:
	python main.py

compile:
	python -m compileall -q app main.py tests

test:
	python -m unittest discover -s tests -v

lint:
	ruff check .

check: compile test

clean:
	python -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
	python -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.ruff_cache', '.mypy_cache'] if pathlib.Path(p).exists()]"