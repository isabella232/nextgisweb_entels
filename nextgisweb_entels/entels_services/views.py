from nextgisweb.resource import resource_factory

from services import (
    store,
    geocollection
)


def setup_pyramid(comp, config):
    config.add_route(
        'nextgisweb_entels.store',
        '/entels/layer/{id:\d+}/store_api/',
        factory=resource_factory).add_view(store)
    config.add_route(
        'nextgisweb_entels.geocollection',
        '/entels/geocollection').add_view(geocollection)
