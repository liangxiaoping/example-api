#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4


class Base(Exception):
    error_code = 500
    error_type = None
    error_message = None
    errors = None

    def __init__(self, *args, **kwargs):
        self.errors = kwargs.pop('errors', None)

        super(Base, self).__init__(*args, **kwargs)

        if len(args) > 0 and isinstance(args[0], basestring):
            self.error_message = args[0]


class Backend(Exception):
    pass


class NotImplemented(Base, NotImplementedError):
    pass


class ConfigurationError(Base):
    error_type = 'configuration_error'


class InvalidObject(Base):
    error_code = 400
    error_type = 'invalid_object'


class BadRequest(Base):
    error_code = 400
    error_type = 'bad_request'


class UnsupportedAccept(BadRequest):
    error_code = 406
    error_type = 'unsupported_accept'


class UnsupportedContentType(BadRequest):
    error_code = 415
    error_type = 'unsupported_content_type'


class Forbidden(Base):
    error_code = 403
    error_type = 'forbidden'


class Duplicate(Base):
    error_code = 409
    error_type = 'duplicate'


class NotFound(Base):
    error_code = 404
    error_type = 'not_found'


class MessageNotFound(NotFound):
    error_type = 'message_not_found'
