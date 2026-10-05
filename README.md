# example-server

A minimal server that follows the patterns of the [Arkitekt](https://arkitekt.live) services:
a Django project with a Strawberry GraphQL API, organization-scoped data, token
verification, typed configuration and a release pipeline. It is a reference to read and a
starting point to copy, not a service a hub installs.

## What it shows

| Pattern | Where |
| --- | --- |
| A model that belongs to an organization, and its GraphQL type | `demo/models.py`, `demo/types.py` |
| Queries, mutations and a subscription | `example_server/schema.py`: `items`, `item`, `createItem`, `updateItem`, `deleteItem`, and the `items` subscription |
| Tokens verified by authentikate | the `authentikate` block of `config.yaml` |
| Typed, validated configuration | `example_server/configuration.py`, documented in [CONFIG.md](CONFIG.md) |
| Tests and a tag-only release as CI workflows | `.github/workflows/` |

GraphQL is served at `/graphql` (HTTP and WebSocket), with the SDL at `/schema`, a health
check at `/ht` and the Django admin at `/admin/`.

One thing it does not show yet: the newer services describe themselves to a hub's installer
through a contract (`python -m arkitekt_service …`) and migrate as a separate step. Here
`run.sh` still waits for the database, migrates and then serves.

## Getting started

```bash
git clone https://github.com/jhnnsrs/example-server.git
cd example-server
docker compose up -d db redis
docker compose run --rm --service-ports example bash run-debug.sh
```

The image has no default command, so the last line names one: `run-debug.sh` waits for the
database, migrates and starts Django's development server. GraphQL is then at
`http://localhost:8888/graphql`.

## Configuration

The service reads `config.yaml`, or the file named by `ARKITEKT_CONFIG_FILE`; any value can
be overridden by an environment variable (`POSTGRES__HOST`). `python manage.py
validate_settings` prints the configuration as the service reads it, with secrets redacted.

See [CONFIG.md](CONFIG.md) for every value.

## Development

```bash
uv sync
uv run pytest
```

The tests run on an in-memory SQLite database and need no Docker. That is enough for the
schema and configuration checks here; a service whose tests write through async GraphQL
needs a real Postgres, as the other Arkitekt services' suites use.

## Releases

Releases are tags: a push to `main` cuts a stable version, a push to `next` a release
candidate. Each one publishes `jhnnsrs/example` under its version, plus `latest` from `main`
and `next` from `next`. The `version` in `pyproject.toml` is a placeholder. Release notes
are on [GitHub Releases](https://github.com/jhnnsrs/example-server/releases).
