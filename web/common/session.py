# -*- coding: utf-8 -*- #
"""
    session.py
    ~~~~~~~~~



    Author:       qianyue
    Date:         2020/3/8 下午9:32
"""
import logging
import uuid
import hmac
import json
import hashlib
import redis

LOGGER = logging.getLogger(__name__)


class SessionData(dict):
    def __init__(self, session_id, hmac_key):
        self.session_id = session_id
        self.hmac_key = hmac_key


class Session(SessionData):
    def __init__(self, session_manager, request_handler):

        self.session_manager = session_manager
        self.request_handler = request_handler

        try:
            current_session = session_manager.get(request_handler)
        except InvalidSessionException:
            current_session = session_manager.get()
        for key, data in current_session.items():
            self[key] = data
        self.session_id = current_session.session_id
        self.hmac_key = current_session.hmac_key

    def save(self):
        self.session_manager.set(self.request_handler, self)


class SessionManager(object):
    def __init__(self, secret, store_options, session_prefix_key, session_timeout):
        self.secret = secret
        self.session_timeout = session_timeout
        self.session_prefix_key = self._utf8(session_prefix_key) if session_prefix_key else self._utf8(
            'tornado-session-')
        redis_host = store_options['redis_host'] if store_options.get('redis_host') else 'localhost'
        redis_port = store_options['redis_port'] if store_options.get('redis_port') else 6379
        redis_password = store_options.get('redis_password')
        if redis_password:
            self.redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
        else:
            self.redis = redis.StrictRedis(host=redis_host, port=redis_port)

    def _fetch(self, session_id):
        try:
            session_data = raw_data = self.redis.get(self.session_prefix_key + session_id)
            if raw_data is not None:
                self.redis.setex((self.session_prefix_key + session_id), self.session_timeout, raw_data)
                session_data = json.loads(raw_data)

            if type(session_data) == dict:
                return session_data
            else:
                return {}
        except IOError:
            return {}

    def get(self, request_handler=None):
        if request_handler is None:
            session_id = None
            hmac_key = None
        else:
            session_id = request_handler.get_secure_cookie("session_id")
            hmac_key = request_handler.get_secure_cookie("verification")
        if session_id is None:
            session_exists = False
            session_id = self._generate_id()
            hmac_key = self._generate_hmac(session_id)
        else:
            session_exists = True
        check_hmac = self._generate_hmac(session_id)
        if hmac_key != check_hmac:
            raise InvalidSessionException()

        session = SessionData(session_id, hmac_key)

        if session_exists:
            session_data = self._fetch(session_id)
            for key, data in session_data.items():
                session[key] = data
        return session

    def set(self, request_handler, session):
        request_handler.set_secure_cookie("session_id", session.session_id)
        request_handler.set_secure_cookie("verification", session.hmac_key)

        session_data = json.dumps(dict(session.items()))
        self.redis.setex((self.session_prefix_key + session.session_id), self.session_timeout, session_data)

    def _generate_id(self):
        sha256 = hashlib.sha256()
        sha256.update(self.secret.encode('utf-8'))
        sha256.update(str(uuid.uuid1()).encode('utf-8'))
        return self._utf8(sha256.hexdigest())

    def _generate_hmac(self, session_id):
        return self._utf8(hmac.new(session_id, self.secret.encode('utf-8'), hashlib.sha256).hexdigest())

    def _utf8(self, value):
        """Converts a string argument to a byte string.

        If the argument is already a byte string or None, it is returned unchanged.
        Otherwise it must be a unicode string and is encoded as utf8.
        """
        if isinstance(value, (bytes, type(None))):
            return value
        if not isinstance(value, str):
            raise TypeError("Expected bytes, unicode, or None; got %r" % type(value))
        return value.encode("utf-8")


class InvalidSessionException(Exception):
    pass
