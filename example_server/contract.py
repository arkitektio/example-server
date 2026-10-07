"""What this image answers a hub's installer: ``arkitekt-service <verb>`` (see ``arkitekt_service.contract``).

The installer knows the hub; how this release spells its config is written here, with the
settings it is read by. A key renamed in ``configuration.py`` is renamed in :func:`render` in
the same commit, and no installer has to learn of it.

This is also the pattern to copy: a service says what it is, how it is started and what
prepares its database in this one module, and there is no start script beside it.
"""

from __future__ import annotations

from arkitekt_service.contract import JSON, Contract, Description, Facts, Job, Needs, Offers, Start, blocks

from example_server.configuration import Settings


def render(facts: Facts) -> dict[str, JSON]:
    """This release's config for the hub ``facts`` describes."""
    return blocks.server(facts)


contract = Contract(
    description=Description(
        name="example",
        identifier="live.arkitekt.example",
        summary="A minimal service, to read and to copy.",
        needs=Needs(),
        offers=Offers(),
    ),
    settings=Settings,
    render=render,
    # How this service is started: there is no script beside it. `arkitekt-service serve`
    # (and `debug`) become these, so they get the container's signals themselves.
    serve=Start(("daphne", "-b", "0.0.0.0", "-p", "80", "--websocket_timeout", "-1", "example_server.asgi:application")),
    debug=Start(("python", "manage.py", "runserver", "0.0.0.0:80")),
    # What else can be run in the image, by name; `setup` is what `run migrate` runs of it.
    jobs={
        "ensureadmin": Job(("ensureadmin",), "Create the operator account the config names"),
    },
    setup=("ensureadmin",),
)
