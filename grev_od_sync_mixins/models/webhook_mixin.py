# -*- coding: utf-8 -*-
"""
Webhook Mixin

Provides a structured foundation for handling webhook callbacks
from external systems.

Usage:
    class SaleOrder(models.Model):
        _inherit = ["sale.order", "webhook.mixin"]

External service calls:
    https://yourdomain.com/webhook/<model_name>
"""

import logging
import hashlib
import hmac
import json

from odoo import api, fields, models, _, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebhookMixin(models.AbstractModel):
    _name = "webhook.mixin"
    _description = "Webhook Handler Mixin"

    # ------------------------------------------------------------
    # Webhook Fields
    # ------------------------------------------------------------
    last_webhook_date = fields.Datetime(
        string="Last Webhook Event",
        readonly=True,
    )

    last_webhook_payload = fields.Text(
        string="Last Webhook Payload",
        readonly=True,
        help="Stores the raw content of the last webhook received."
    )

    webhook_status = fields.Selection(
        [
            ("none", "None"),
            ("received", "Received"),
            ("processed", "Processed"),
            ("failed", "Failed"),
        ],
        default="none",
        readonly=True,
    )

    # Optional: secret used to validate webhook signatures
    webhook_secret = fields.Char(
        string="Webhook Secret",
        help="Secret used to validate webhook HMAC signatures.",
    )

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------
    def process_webhook(self,  payload: dict, raw_payload: str):
        """
        Process webhook payload.
        MUST be implemented in child classes.

        `payload` = dict parsed from JSON webhook body.
        """
        raise NotImplementedError(
            _("You must implement process_webhook() in your inheriting model.")
        )

    # ------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------
    def _update_webhook_metadata(self, payload, status="received"):
        """Stores payload and updates timestamps."""
        self.write({
            "last_webhook_date": fields.Datetime.now(),
            "last_webhook_payload": json.dumps(payload, indent=2),
            "webhook_status": status,
        })

    def _validate_signature(self, raw_body: bytes, signature: str) -> bool:
        """
        Validate HMAC signature if 'webhook_secret' is defined.
        """
        self.ensure_one()
        if not self.webhook_secret:
            return True

        computed = hmac.new(
            self.webhook_secret.encode("utf-8"),
            raw_body,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(computed, signature or "")


