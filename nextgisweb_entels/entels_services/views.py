from nextgisweb.resource import resource_factory

from services import (
    store,
    geocollection
)


def setup_pyramid(comp, config):
    config.add_route(
        'nextgisweb_entels.store',
        '/layer/{id:\d+}/store_api/entels',
        factory=resource_factory).add_view(store)
    config.add_route(
        'nextgisweb_entels.geocollection',
        '/geocollection/entels').add_view(geocollection)
