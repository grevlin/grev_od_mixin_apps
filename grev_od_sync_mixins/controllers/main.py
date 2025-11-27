import logging
import hashlib
import hmac
import json

from odoo import api, fields, models, _, http
from odoo.http import request

_logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# HTTP Controller
# ------------------------------------------------------------

class WebhookController(http.Controller):
    """
    Universal webhook endpoint.

    URL format:
      /webhook/<model>
    """

    @http.route(["/webhook/<string:api_name>","/webhook/<string:api_name>/<string:backend_token>"], type="jsonrpc", auth="public", methods=["POST"], csrf=False)
    def handle_webhook(self, api_name,backend_token=None, **kwargs):
        if hasattr(self,f'{api_name}_handle_webhook'):
            return getattr(self,f'{api_name}_handle_webhook')(backend_token,**kwargs)
        
        return {"error": "webhooks Not supported"}
