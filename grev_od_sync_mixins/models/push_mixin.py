# -*- coding: utf-8 -*-
"""
Push Mixin

Provides helpers for exporting records from Odoo to an external system.

Usage:
    class ProductTemplate(models.Model):
        _inherit = ["product.template", "push.mixin"]
"""

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PushMixin(models.AbstractModel):
    _name = "push.mixin"
    _description = "Push Synchronization Mixin"

    # Generic sync fields used by connectors
    last_push_date = fields.Datetime(
        string="Last Push Date",
        readonly=True,
        help="Timestamp of the last successful push to the external system.",
    )

    last_push_status = fields.Selection(
        [
            ("success", "Success"),
            ("failed", "Failed"),
            ("pending", "Pending"),
        ],
        string="Last Push Status",
        default="pending",
        readonly=True,
    )

    push_error_message = fields.Text(
        string="Last Push Error",
        readonly=True,
    )

    external_id = fields.Char(
        string="External ID",
        help="Identifier of this record in the external system.",
    )

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------
    def push(self, raise_on_error=False):
        """
        Public method to trigger push to external system.
        Handles tracking of logs, errors and status.

        Parameters
        ----------
        raise_on_error: bool
            If True, errors will be raised as Odoo exceptions.
        """
        for record in self:
            try:
                _logger.info("Pushing record ID %s (%s)", record.id, record._name)

                # Execute custom export logic implemented by child class
                export_data = record._prepare_push_payload()
                response = record._push_to_external(export_data)

                # Handle success
                record._handle_push_success(response)

            except Exception as e:
                _logger.error("Push failed for %s ID %s: %s",
                              record._name, record.id, str(e), exc_info=True)
                record._handle_push_failure(e)

                if raise_on_error:
                    raise UserError(_("Push failed: %s") % e)

        return True

    # ------------------------------------------------------------
    # Overridable methods
    # ------------------------------------------------------------
    def _prepare_push_payload(self):
        """
        Return a dict representing data to send to external system.

        MUST be implemented in the inheriting model.
        """
        raise NotImplementedError(
            _("_prepare_push_payload must be implemented in the inheriting model.")
        )

    def _push_to_external(self, payload):
        """
        Send data to the external API.

        MUST be overridden to perform the actual HTTP/API call.
        Should return the API's response.
        """
        raise NotImplementedError(
            _("_push_to_external must be implemented in the inheriting model.")
        )

    # ------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------
    def _handle_push_success(self, response):
        """Executed when push succeeds."""
        self.write({
            "last_push_date": fields.Datetime.now(),
            "last_push_status": "success",
            "push_error_message": False,
        })

        # Extract external_id if provided by the remote service
        if isinstance(response, dict) and response.get("external_id"):
            self.external_id = response["external_id"]

        _logger.info("Successfully pushed %s ID %s", self._name, self.id)

    def _handle_push_failure(self, exception):
        """Executed when push fails."""
        self.write({
            "last_push_date": fields.Datetime.now(),
            "last_push_status": "failed",
            "push_error_message": str(exception),
        })
