.venv: pyproject.toml
	python -m virtualenv .venv

.venv/deps: .venv pyproject.toml setup.cfg
	.venv/bin/python -m pip install . build pytest twine attrs
	touch .venv/deps

build: .venv/deps
	rm -rf ./dist/
	.venv/bin/python -m build .

# only works with python 3+
lint: .venv/deps
	.venv/bin/python -m pip install black==22.3.0
	.venv/bin/python -m black .

lint-check: .venv/deps
	.venv/bin/python -m pip install black==22.3.0
	.venv/bin/python -m black --check .

test: .venv/deps
	.venv/bin/python -m pytest jsonschema_extractor -vv

ready-pr: test lint