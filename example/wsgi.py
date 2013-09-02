#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

from example.openstack.common import wsgi


class Middleware(wsgi.Middleware):
    @classmethod
    def factory(cls, global_config, **local_conf):
        """ Used for paste app factories in paste.deploy config files """

        def _factory(app):
            return cls(app, **local_conf)

        return _factory
