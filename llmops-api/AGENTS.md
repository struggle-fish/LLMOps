# Repository Guidelines

## Project Structure & Module Organization

This repository is a Flask-based Python API. The application bootstrap is in
`app/http/app.py`; it loads `.env`, configures dependency injection, and creates
the Flask server. Business code lives under `internal/`, organized by layer:
`router/` for routes, `handler/` for controllers, `service/` for business
logic, `model/` for database models, `schema/` for request/response schemas,
and `extension/` for Flask integrations. Shared infrastructure belongs in
`pkg/` (for example, response and SQLAlchemy helpers). Database migrations are
under `internal/migrations/`, tests under `test/`, learning experiments under
`study/`, and local files under `storage/`.

## Build, Test, and Development Commands

There is no separate build script in this repository. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.http.app           # Run the Flask server locally
pytest                           # Run the full test suite
pytest test/internal/handler      # Run a focused test area
```

Keep dependency changes in `requirements.txt` and avoid committing virtual
environments or generated files.

## Coding Style & Naming Conventions

Use Python with four-space indentation, readable type hints, and short
docstrings or Chinese comments for non-obvious business logic. Use `snake_case`
for modules, functions, variables, and test files; use `PascalCase` for
classes. Preserve the existing layering: routes call handlers, handlers call
services, and request validation belongs in schemas rather than route code.
No repository-wide formatter or linter is configured, so keep changes
consistent with neighboring files.

## Testing Guidelines

Tests use pytest and are named `test_*.py`; test classes use `Test*`. Reuse the
shared fixtures in `test/conftest.py`. Add or update focused tests for changed
handlers, validation, services, and response codes. Run `pytest` before opening
a pull request; no coverage threshold is currently configured.

## Configuration & Security

Use `.env` for local secrets and provider settings; never commit API keys,
tokens, or database credentials. Review migration changes carefully and keep
schema updates reversible where practical.

## Commit & Pull Request Guidelines

Existing commits use short, descriptive summaries, including concise Chinese
messages. Keep commits focused and use an imperative subject. Pull requests
should explain the behavior change, list validation commands, link related
issues, and call out API, configuration, or migration changes. Include request/
response examples or screenshots when they clarify an endpoint change.
