#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

import flask


def factory(global_config, **local_conf):
    app = flask.Flask('example.api.versions')

    @app.route('/', methods=['GET'])
    def version_list():
        versions = [dict(id="v1", status="CURRENT")]
        return flask.jsonify(dict(versions=versions))

    return app
