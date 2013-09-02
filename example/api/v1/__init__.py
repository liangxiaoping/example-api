#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
import flask
from stevedore import extension
from werkzeug import exceptions as wexceptions
from werkzeug import wrappers


from example.openstack.common import jsonutils as json
from example.openstack.common import log as logging
from example import exceptions

LOG = logging.getLogger(__name__)


class Request(flask.Request, wrappers.AcceptMixin,
              wrappers.CommonRequestDescriptorsMixin):
    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)

        self._validate_content_type()
        self._validate_accept()

    def _validate_content_type(self):
        if (self.method in ['POST', 'PUT', 'PATCH']
                and self.mimetype != 'application/json'):

            msg = 'Unsupported Content-Type: %s' % self.mimetype
            raise exceptions.UnsupportedContentType(msg)

    def _validate_accept(self):
        if 'accept' in self.headers and not self.accept_mimetypes.accept_json:
            msg = 'Unsupported Accept: %s' % self.accept_mimetypes
            raise exceptions.UnsupportedAccept(msg)


def factory(global_config, **local_conf):
    app = flask.Flask('example.api.v1')
    app.request_class = Request
    app.config.update(PROPAGATE_EXCEPTIONS=True)

    # disable strict slashes.  This allows trailing slashes in the URLS.
    app.url_map.strict_slashes = False

    # Ensure all error responses are JSON
    def _json_error(ex):
        code = ex.code if isinstance(ex, wexceptions.HTTPException) else 500

        response = {'code': code}
        if code == 405:
            response['type'] = 'invalid_method'

        response = flask.jsonify(**response)
        response.status_code = code
        return response

    for code in wexceptions.default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = _json_error

    def _register_blueprint(ext):
        app.register_blueprint(ext.plugin)

    # Add all in-built APIs
    mgr = extension.ExtensionManager('example.api.v1')
    mgr.map(_register_blueprint)

    return app
