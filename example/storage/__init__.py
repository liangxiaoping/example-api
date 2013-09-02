#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

from oslo.config import cfg
from example.openstack.common import importutils
from example.openstack.common import log as logging
from example.storage.base import Storage

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

cfg.CONF.register_opts([
    cfg.StrOpt('storage_driver', 
               default='example.storage.impl_redis.RedisStorage',
               help='Storage driver'),
])


STORAGE_DRIVER = None

def get_storage():
    global STORAGE_DRIVER
    if STORAGE_DRIVER is None:
        STORAGE_DRIVER = importutils.import_object(CONF.storage_driver)
    return STORAGE_DRIVER
