# -*- coding: utf-8 -*-
from nextgisweb.component import Component


@Component.registry.register
class EntelsServicesComponent(Component):
    identity = 'entels_services'

    def initialize(self):
        super(EntelsServicesComponent, self).initialize()

    def setup_pyramid(self, config):
        super(EntelsServicesComponent, self).setup_pyramid(config)

        from . import views
        views.setup_pyramid(self, config)

    settings_info = ()
