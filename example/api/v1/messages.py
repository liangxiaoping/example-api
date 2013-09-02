#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

import flask

from oslo.config import cfg
from example import exceptions
from example.openstack.common import log as logging
from example.storage import api

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
blueprint = flask.Blueprint('messages', __name__)
#storage_api = api.StorageAPI()

message_opts = []
CONF.register_opts(message_opts)


@blueprint.route('/messages', methods=['POST'])
def create_message():
    context = flask.request.environ.get('context')
    body = flask.request.json

    return flask.Response(status=200)

@blueprint.route('/messages/<message_id>', methods=['GET'])
def get_message(message_id):
    context = flask.request.environ.get('context')
    
    #messages = storage_api.get_message(context, message_id)

    return flask.jsonify(messages=[])

@blueprint.route('/messages/<message_id>', methods=['PUT'])
def update_message(message_id):
    context = flask.request.environ.get('context')
    body = flask.request.json

    return flask.Response(status=200)

@blueprint.route('/messages/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    context = flask.request.environ.get('context')
    
    return flask.Response(status=200)


