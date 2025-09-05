alias i := install
alias s := serve
alias b := build
alias t := test
alias tc := test-cov
alias c := check

init:
    just install
    uv run pre-commit install --install-hooks

install:
    uv sync

serve:
    uv run mkdocs serve

build:
    uv run mkdocs build

test:
    uv run pytest -vv

test-cov:
    uv run pytest --cov={{ justfile_directory() }}/rubik_algorithm \
      --cov={{ justfile_directory() }}/tests \
      --cov-report=html \
      --cov-config={{ justfile_directory() }}/pyproject.toml \
      -vv

check:
    uv run pre-commit run -a
