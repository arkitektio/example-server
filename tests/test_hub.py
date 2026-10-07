"""The image, proven in a hub made for the test: described, configured, prepared, served, talked to.

End to end, and not part of the default run (``addopts`` leaves ``hub`` out): it needs Docker,
``konstruktor`` and a built image.

    pytest -m hub --service-image example:dev
"""

import pytest
from arkitekt_service.testing import ServiceHub, check_service


@pytest.mark.hub
def test_the_image_runs_in_a_hub(service_hub: ServiceHub) -> None:
    """What every service has to answer: ready, healthy, closed to nobody, open to an app of the hub, fully migrated, never restarted."""
    check_service(service_hub)
