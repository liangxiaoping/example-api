#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

from example import storage
from example.openstack.common import log as logging
from example.openstack.common import excutils
LOG = logging.getLogger(__name__)


class StorageAPI(object):
    """ Storage API """

    def __init__(self):
        self.storage = storage.get_storage()

    # message
    def create_message(self, context, *args, **kwargs):
        try:
            return self.storage.create_message(context, *args, **kwargs)
        except Exception as exc:
            LOG.error("Create message failed due to %s" % exc)
            with excutils.save_and_reraise_exception():
                pass

