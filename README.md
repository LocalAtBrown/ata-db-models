# ata-db-models

<!-- [![Release](https://img.shields.io/github/v/release/LocalAtBrown/ata-db-models)](https://img.shields.io/github/v/release/LocalAtBrown/ata-db-models) -->
<!-- [![Build status](https://img.shields.io/github/workflow/status/LocalAtBrown/ata-db-models/merge-to-main)](https://img.shields.io/github/workflow/status/LocalAtBrown/ata-db-models/merge-to-main) -->

[![Python version](https://img.shields.io/badge/python_version-3.9-blue)](https://github.com/psf/black)
[![Code style with black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)
[![More style with flake8](https://img.shields.io/badge/code_style-flake8-blue)](https://flake8.pycqa.org)
[![Imports with isort](https://img.shields.io/badge/%20imports-isort-blue)](https://pycqa.github.io/isort/)
[![Type checking with mypy](https://img.shields.io/badge/type_checker-mypy-blue)](https://mypy.readthedocs.io)
[![License](https://img.shields.io/github/license/LocalAtBrown/ata-db-models)](https://img.shields.io/github/license/LocalAtBrown/ata-db-models)

Database models and migrations for Automating the Ask.

## Usage

### As a package

We use [SQLModel](https://sqlmodel.tiangolo.com/), a layer on top of SQLAlchemy with Pydantic, to define our tables.
This is useful because we can import this package to interact with the tables AND have Pydantic objects in Python
that correspond to a row in the table.

To install the package from PyPi, run: `pip install ata-db-models`. Check existing versions 
[here](https://pypi.org/project/ata-db-models/).

### Initialize a new cluster

If you want to initialize a fresh database cluster, pass in the env vars to connect to the cluster and run `init_db`.
If the target cluster has IP restrictions, make sure your IP address is a valid access point.

An example run with fake credentials (from the root dir of this project with the virtual env
activated):
`HOST=fakehost USER=fakeuser PASSWORD=fakepw DB_NAME=postgres python src/init_db.py`

No `PORT` is passed because the default port is 5432, the standard for Postgres.

### Migrations

So you made some changes to what tables there are, what columns there are, indices, etc. and you'd like to
update the databases. This is what alembic is for!

 TODO ALEMBIC INSTRUCTIONS

## Development

This project uses [Poetry](https://python-poetry.org/) to manage dependencies. It also helps with pinning dependency and python
versions. We also use [pre-commit](https://pre-commit.com/) with hooks for [isort](https://pycqa.github.io/isort/),
[black](https://github.com/psf/black), and [flake8](https://flake8.pycqa.org/en/latest/) for consistent code style and
readability. Note that this means code that doesn't meet the rules will fail to commit until it is fixed.

We use [mypy](https://mypy.readthedocs.io/en/stable/index.html) for static type checking. This can be run [manually](#run-static-type-checking),
and the CI runs it on PRs to the `main` branch. We also use [pytest](https://docs.pytest.org/en/7.2.x/) to run our tests.
This can be run [manually](#run-tests) and the CI runs it on PRs to the `main` branch.

### Setup

1. [Install Poetry](https://python-poetry.org/docs/#installation).
2. Run `poetry install --no-root`
3. Run `source $(poetry env list --full-path)/bin/activate && pre-commit install && deactivate` to set up `pre-commit`

You're all set up! Your local environment should include all dependencies, including dev dependencies like `black`.
This is done with Poetry via the `poetry.lock` file.

### Run Code Format and Linting

To manually run isort, black, and flake8 all in one go, simply run `pre-commit run --all-files`. Explore the `pre-commit` docs (linked above)
to see more options.

### Run Static Type Checking

To manually run mypy, simply run `mypy` from the root directory of the project. It will use the default configuration
specified in `pyproject.toml`.

### Update Dependencies

To update dependencies in your local environment, make changes to the `pyproject.toml` file then run `poetry update` from the root directory of the project.

### Run Tests

To manually run rests, you need to have a Postgres instance running locally on port 5432. One way to do this
is to run a Docker container, then run the tests while it is active.

1. (If you don't already have the image locally) Run `docker pull postgres`
2. Run `docker run --rm --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_HOST_AUTH_METHOD=trust -p 127.0.0.1:5432:5432/tcp postgres`
3. Run `DB_NAME=postgres pytest tests` from the root directory of the project. Explore the `pytest` docs (linked above)
to see more options.

Note that if you decide to run the Postgres container with different credentials (a different password, port, etc.) or
via a different method, you will likely need to update the test file to point to the correct Postgres instance.

Additionally, if you want to re-run the tests, you want to make sure you start over from a fresh Postgres
instance. If you run Postgres via Docker, you can simply `ctrl-C` to stop the image and start a new one.
