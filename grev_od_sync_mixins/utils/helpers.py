from uuid import uuid4
import requests
import json
import logging
from contextlib import contextmanager
from functools import wraps
from requests import HTTPError
from odoo.modules.registry import Registry
from odoo.sql_db import BaseCursor
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

def requires_auth_token(func):
    def wrapped(self, *args, **kwargs):
        if not kwargs.get('token'):
            raise AttributeError("An authentication token is required")
        return func(self, *args, **kwargs)
    return wrapped


def after_commit(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        assert isinstance(self.env.cr, BaseCursor)
        dbname = self.env.cr.dbname
        context = self.env.context
        uid = self.env.uid

        if self.env.context.get('no_sync'):
            return

        @self.env.cr.postcommit.add
        def called_after():
            db_registry = Registry(dbname)
            with db_registry.cursor() as cr:
                env = api.Environment(cr, uid, context)
                try:
                    func(self.with_env(env), *args, **kwargs)
                except Exception as e:
                    _logger.warning("Could not sync record now: %s" % self)
                    _logger.exception(e)

    return wrapped


@contextmanager
def needed_token(user):
    yield user._get_needed_token()