#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

import flask
from oslo.config import cfg
from example.openstack.common import jsonutils as json


cfg.CONF.register_opts([
    cfg.IntOpt('api_workers', default=None,
               help='Number of worker processes to spawn'),
    cfg.StrOpt('api_host', default='0.0.0.0',
               help='API Host'),
    cfg.IntOpt('api_port', default=16379,
               help='API Port Number'),
    cfg.StrOpt('api_paste_config', default='api-paste.ini',
               help='File name for the paste.deploy config for example-api'),
    cfg.StrOpt('auth_strategy', default='noauth',
               help='The strategy to use for auth. Supports noauth or '
                    'keystone'),
])


# Allows us to serialize datetime's etc
flask.helpers.json = json
