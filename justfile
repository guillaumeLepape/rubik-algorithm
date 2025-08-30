alias s := setup
alias i := install
alias t := test
alias tc := test-cov
alias c := check

setup:
    just install
    uv run pre-commit install --install-hooks

install:
    uv sync --all-extras --all-groups

test:
    uv run pytest -vv

test-cov:
    uv run pytest --cov={{ justfile_directory() }}/yak_server \
      --cov={{ justfile_directory() }}/scripts \
      --cov={{ justfile_directory() }}/tests \
      --cov={{ justfile_directory() }}/testing \
      --cov-report=html \
      --cov-config={{ justfile_directory() }}/pyproject.toml \
      -vv

check:
    uv run pre-commit run -a
