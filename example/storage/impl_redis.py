#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

import redis
import eventlet
import functools

from oslo.config import cfg

from example import utils
from example.openstack.common import log as logging
from example.openstack.common import uuidutils
from example.openstack.common import timeutils
from example.storage import base

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
REDIS_CLIENT = None

redis_opts = [
    cfg.StrOpt('redis_host',
               default='0.0.0.0',
               help='Redis Host'),
    cfg.IntOpt('redis_port',
               default=6379,
               help='Redis Port Number'),
    cfg.FloatOpt('redis_lock_timeout',
                default=120,
                help='Redis Lock Timeout'),
]

CONF.register_opts(redis_opts)


def get_client():
    global REDIS_CLIENT
    if REDIS_CLIENT is None:
        REDIS_CLIENT = redis.Redis(CONF.redis_host, CONF.redis_port)
    return REDIS_CLIENT


def with_lock(func):
    @functools.wraps(func)
    def __inner(self, context, key, *args, **kwargs):
        client = get_client()
        with client.lock(key, timeout=CONF.redis_lock_timeout):
            return func(self, context, key, *args, **kwargs)
    return __inner


class RedisStorage(base.Storage):
    def __init__(self):
        super(RedisStorage, self).__init__()
        self.client = get_client()

    # message
    def create_messages(self, context, *args, **kwargs)
        pass
