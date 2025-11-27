from datetime import datetime
import logging
import time
import json
import requests
from werkzeug import urls
from typing import Dict, List, Optional, Tuple
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ApiServiceMixin(models.AbstractModel):
    _name = 'api.service.mixin'
    _description = 'API Service Mixin'
    _service_name = 'api'
    _service_auth_endpoint = ''
    _service_token_endpoint = ''
    _api_base_url = ''

    def _revoke_oauth_tokens(self):
        raise NotImplementedError(
            _("must be implemented in the inheriting model.")
        )

    def _set_oauth_tokens(self, access_token: str, refresh_token: str, expires_in: int, owner: str = None, organization: str = None):
        raise NotImplementedError(
            _("must be implemented in the inheriting model.")
        )

    def oauth_authorize_url(self, scope: str = "default") -> str:
        raise NotImplementedError(
            _("must be implemented in the inheriting model.")
        )

    def oauth_exchange_code(self, code: str) -> Dict:
        raise NotImplementedError(
            _("must be implemented in the inheriting model.")
        )

    def oauth_revoke(self) -> Dict:
        raise NotImplementedError(
            _("must be implemented in the inheriting model.")
        )

    def oauth_refresh(self) -> Dict:
        raise NotImplementedError(
            _("must be implemented in the inheriting model.")
        )

    def _get_headers(self) -> Dict[str, str]:
        raise NotImplementedError(
            _("must be implemented in the inheriting model.")
        )
        
    def _request(self, method: str, url: str, params: Optional[Dict] = None, data: Optional[Dict] = None):
        headers = self._get_headers()
        backoff = 1.0
        for attempt in range(5):
            resp = requests.request(
                method, url, headers=headers, params=params, json=data, timeout=30)
            if resp.status_code == 429:
                time.sleep(backoff)
                backoff = min(backoff * 2.0, 10.0)
                continue
            if resp.status_code >= 400:
                raise UserError(_("%s API error %s: %s") %
                                (self._service_name,resp.status_code, resp.text))
            return resp.json()
        raise UserError(_("%s API rate-limited repeatedly") % self._service_name)

    def _get_client_secret(self):
        ICP = self.env['ir.config_parameter'].sudo()
        return ICP.get_param('%s_client_secret' % self._service_name)

    def _get_client_id(self):
        ICP = self.env['ir.config_parameter'].sudo()
        return ICP.get_param('%s_client_id' % self._service_name)

    

    @api.model
    def _get_tokens(self, authorize_code, scope,  redirect_uri):
        return

    def _refresh_token(self, rtoken):
        return
