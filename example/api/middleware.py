#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

import flask
import webob.dec
from oslo.config import cfg

from example import exceptions
from example.openstack.common import local
from example.openstack.common import log as logging
from example.openstack.common import jsonutils as json
from example.openstack.common import uuidutils
from example.openstack.common import context as common_context
from example import wsgi

LOG = logging.getLogger(__name__)


def auth_pipeline_factory(loader, global_conf, **local_conf):
    """
    A paste pipeline replica that keys off of auth_strategy.

    Code nabbed from cinder.
    """
    pipeline = local_conf[cfg.CONF.auth_strategy]
    pipeline = pipeline.split()
    filters = [loader.get_filter(n) for n in pipeline[:-1]]
    app = loader.get_app(pipeline[-1])
    filters.reverse()
    for filter in filters:
        app = filter(app)
    return app


class FaultWrapperMiddleware(wsgi.Middleware):
    def __init__(self, application):
        super(FaultWrapperMiddleware, self).__init__(application)

        LOG.info('Starting faultwrapper middleware')

    @webob.dec.wsgify
    def __call__(self, request):
        try:
            return request.get_response(self.application)
        except exceptions.Base as e:
            # Handle Athena Exceptions
            status = e.error_code if hasattr(e, 'error_code') else 500

            # Start building up a response
            response = {'code': status}

            if e.error_type:
                response['type'] = e.error_type

            if e.error_message:
                response['message'] = e.error_message

            if e.errors:
                response['errors'] = e.errors

            return self._handle_exception(request, e, status, response)
        except Exception as e:
            # Handle all other exception types
            return self._handle_exception(request, e)

    def _handle_exception(self, request, e, status=500, response={}):
        # Log the exception ASAP
        LOG.exception(e)

        headers = [('Content-Type', 'application/json'),]

        # Set a response code and type, if they are missing.
        if 'code' not in response:
            response['code'] = status

        if 'type' not in response:
            response['type'] = 'unknown'

        # Set the request ID, if we have one
        if 'context' in request.environ:
            response['request_id'] = request.environ['context'].request_id

        # Return the new response
        return flask.Response(status=status, headers=headers,
                              response=json.dumps(response))


class ContextMiddleware(wsgi.Middleware):
    def process_response(self, response):
        try:
            context = local.store.context
        except Exception:
            pass
        else:
            # Add the Request ID as a response header
            response.headers['X-Request-ID'] = context.request_id

        return response


class NoAuthContextMiddleware(ContextMiddleware):
    def __init__(self, application):
        super(NoAuthContextMiddleware, self).__init__(application)

        LOG.info('Starting noauthcontext middleware')

    def process_request(self, request):
        # NOTE(kiall): This makes the assumption that disabling authentication
        #              means you wish to allow full access to everyone.
        context = common_context.RequestContext(is_admin=True)

        # Store the context where oslo-log exepcts to find it.
        local.store.context = context

        # Attach the context to the request environment
        request.environ['context'] = context
