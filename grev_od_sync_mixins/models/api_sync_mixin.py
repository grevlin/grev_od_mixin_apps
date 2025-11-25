import logging
from contextlib import contextmanager
from functools import wraps
from requests import HTTPError
import pytz
from dateutil.parser import parse
from markupsafe import Markup

from odoo import api, fields, models, _
from odoo.fields import Domain
from odoo.modules.registry import Registry
from odoo.tools import email_normalize
from odoo.sql_db import BaseCursor

from ..utils.helpers import after_commit

_logger = logging.getLogger(__name__)


class ApiSyncMixin(models.AbstractModel):
    _name = 'api.sync.mixin'
    _description = 'API Sync Mixin'

    external_id = fields.Char(
        'Resource Id in Remote API', index='btree_not_null', copy=False)
    need_sync = fields.Boolean(default=True, copy=False)
    active = fields.Boolean(default=True)

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------
    def set_external_id(self, external_id):
        """
        Assign an external ID to the record.
        """
        self.ensure_one()
        self.external_id = external_id
        return True

    def clear_external_id(self):
        """
        Remove the linked external ID from the record.
        """
        self.ensure_one()
        self.external_id = False
        return True

    def has_external_id(self):
        """
        Returns True if record is linked to a remote identifier.
        """
        self.ensure_one()
        return bool(self.external_id)

    def update_external_sync_date(self):
        """
        Update the timestamp for last sync.
        """
        self.external_last_sync = fields.Datetime.now()
        return True

    @api.model
    def find_or_create(self, recordset,**kwargs):
        pass

    @api.model
    def _parse_iso(self, value: str):
        if not value:
            return False
        try:
            # Normalize ISO8601 to Odoo datetime string (UTC)
            from datetime import datetime
            import dateutil.parser  # type: ignore

            dt = dateutil.parser.isoparse(value)
            # Odoo expects naive UTC string
            return fields.Datetime.to_string(dt)
        except Exception:
            # Fallback: best-effort
            return (value[:19] or "").replace("T", " ")
