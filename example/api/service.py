#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

from paste import deploy
from oslo.config import cfg

from example.openstack.common import log as logging
from example.openstack.common import wsgi
from example import exceptions
from example import utils


LOG = logging.getLogger(__name__)


class Service(wsgi.Service):
    def __init__(self, backlog=128, threads=1000):

        api_paste_config = cfg.CONF.api_paste_config
        config_paths = utils.find_config(api_paste_config)

        if len(config_paths) == 0:
            msg = 'Unable to determine appropriate api-paste-config file'
            raise exceptions.ConfigurationError(msg)

        LOG.info('Using api-paste-config found at: %s' % config_paths[0])

        application = deploy.loadapp("config:%s" % config_paths[0],
                                     name='example_api')

        super(Service, self).__init__(application=application,
                                      host=cfg.CONF.api_host,
                                      port=cfg.CONF.api_port,
                                      backlog=backlog,
                                      threads=threads)
