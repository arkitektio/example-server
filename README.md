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
| What it tells an installer, and how it is started | `example_server/contract.py` |
| Tests and a tag-only release as CI workflows | `.github/workflows/` |

GraphQL is served at `/graphql` (HTTP and WebSocket), with the SDL at `/schema`, a health
check at `/ht` and the Django admin at `/admin/`.

It also describes itself to a hub's installer, as every service does
(`example_server/contract.py`): what it is, how it is started, and what prepares its
database. Everything done with its image goes through one command, `arkitekt-service`, and
there is no start script.

## Getting started

```bash
git clone https://github.com/arkitektio/example-server.git
cd example-server
docker compose up -d db redis
docker compose run --rm --service-ports example arkitekt-service standalone --debug
```

Started with no command the image only says what it is, so the last line names one:
`standalone --debug` waits for the database, migrates, creates the admin account and starts
Django's development server. An installer does the two halves apart (`arkitekt-service run
migrate` once per release, then `arkitekt-service serve`). GraphQL is then at
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
are on [GitHub Releases](https://github.com/arkitektio/example-server/releases).
