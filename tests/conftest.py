"""Shared pytest fixtures for the example service.

The key fixture is ``authenticated_context``: it builds a kante ``HttpContext``
whose request already carries a user/client/organization matching the static
``test`` token (see ``settings_test``), so the schema's ``AuthentikateExtension``
authenticates as that identity at resolve time.
"""

import pytest
from authentikate.models import Client, Membership, Organization, User
from kante.context import HttpContext, UniversalRequest
from strawberry.http.temporal_response import TemporalResponse

from example_server.schema import schema

#: `service_hub` and the `hub` marker: a hub made for the test, running this service's image
#: (`tests/test_hub.py`).
pytest_plugins = ["arkitekt_service.testing"]


@pytest.fixture
def authenticated_context(db) -> HttpContext:
    """An HTTP context authenticated as the static ``test`` token's identity."""
    user, _ = User.objects.get_or_create(sub="1", iss="static_issuer", defaults={"username": "static_issuer_1"})
    client, _ = Client.objects.get_or_create(client_id="oinsoins")
    org, _ = Organization.objects.get_or_create(slug="static_org")
    membership, _ = Membership.objects.get_or_create(user=user, organization=org)

    request = UniversalRequest(
        _extensions={"token": "test"},
        _client=client,  # type: ignore
        _user=user,  # type: ignore
        _organization=org,  # type: ignore
    )
    request.set_membership(membership)  # type: ignore

    return HttpContext(
        request=request,
        response=TemporalResponse(),
        headers={"Authorization": "Bearer test"},
        type="http",
    )


@pytest.fixture
def aexecute(authenticated_context):
    """Run a GraphQL document against the schema, defaulting to the authed context."""

    async def _run(query, variables=None, context=None):
        return await schema.execute(
            query,
            variable_values=variables or {},
            context_value=context or authenticated_context,
        )

    return _run
