alias s := setup
alias i := install
alias r := run
alias t := test
alias tc := test-cov
alias c := check

setup:
    just install
    uv run pre-commit install --install-hooks

install:
    uv sync --all-extras --all-groups

run:
    uv run uvicorn --reload --factory rubik.app:create_app

test:
    uv run pytest -vv

test-cov:
    uv run pytest --cov={{ justfile_directory() }}/rubik \
      --cov={{ justfile_directory() }}/tests \
      --cov-report=html \
      --cov-config={{ justfile_directory() }}/pyproject.toml \
      -vv

check:
    uv run pre-commit run -a
