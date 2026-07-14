# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python test automation framework targeting the [Silpo](https://silpo.ua) e-commerce site (Ukrainian grocery
retailer) and the [Petstore Swagger API](https://petstore.swagger.io/). It combines Playwright-based UI tests and
httpx-based API tests, both run via pytest.

## Setup

```bash
pip install -r requirements.txt
playwright install
```

Copy `config/.env.example` to `config/.env.local` and fill in the required values:

- `BASE_UI_URL` — base URL for Playwright tests
- `BASE_API_URL` — base URL for API tests (default: `https://petstore.swagger.io/`)
- `BROWSER` — `CHROME` or `FIREFOX`
- `AUTH_KEY` — API auth key

The `ENV` environment variable controls which `.env.<ENV>` file is loaded from `config/`. Defaults to `local`.

## Running Tests

```bash
# Run all tests (headed, with Allure reporting — as configured in pyproject.toml)
pytest

# Run a single test by name
pytest -s -k test_name

# Run in parallel (3 workers)
pytest -n 3

# Debug mode (opens Playwright inspector)
$env:PWDEBUG=1; pytest -s -k test_name

# View a trace file
playwright show-trace trace.zip

# Generate and open Allure report
allure serve allure-results
```

## Architecture

### Configuration (`config.py`)

`Settings` is a `pydantic-settings` `BaseSettings` class loaded from `config/.env.<ENV>`. All test code imports
`from config import settings` to access `BASE_API_URL`, `BASE_UI_URL`, `BROWSER`, etc.

### API Layer (`API/`)

- `API_Client` — thin `httpx.Client` wrapper (context manager) with `base_url` from settings. Used as a module-scoped
  pytest fixture.
- `PetModels.py` — Pydantic models for request/response validation (`PetCreateModelRequest`, `PetCreateModelResponse`,
  `PetErrorResponse`) and the `PetStatus` enum.

### UI Layer (`POM/`)

Page Object Model hierarchy:

- `BaseActions` — low-level helpers (e.g., `click_first_visible`) that wrap raw Playwright `Page`
- `BasePage` — composes shared components (`Header`, `Menu`) and a `DataBase` instance; all page objects inherit from it
- `POM/Pages/` — page-specific classes (`MainPage`, `RecepyPage`) that extend `BasePage` and return other page objects
  from navigation actions
- `POM/components/` — reusable UI component classes (`Header`, `Menu`) that extend `BaseActions`

### Tests

- `Test/TestApi.py` — API tests using the `api_client` fixture and Pydantic model validation
- `tries/` — exploratory/scratch tests (Silpo UI, EPAM); not part of the main test suite

### Fixtures (UI)

Browser lifecycle fixtures live in `tries/conftest.py` and provide `browser_context`, `page`, and `open_page` (navigates
to `/` and injects a cookie to bypass the cookie consent banner). An `authorized` fixture injects a JWT `access_token`
into `localStorage`.
