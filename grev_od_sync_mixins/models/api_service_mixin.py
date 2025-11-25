from datetime import datetime
import logging

import json
import requests
from werkzeug import urls

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ApiServiceMixin(models.AbstractModel):
    _name = 'api.service.mixin'
    _description = 'API Service Mixin'
    _service_name = 'api'
    _service_auth_endpoint = ''
    _service_token_endpoint = ''

    def _do_request(self, uri, params=None, headers=None, method='POST', preuri='', timeout=30):
        """ Execute the request to an external API. Return a tuple ('HTTP_CODE', 'HTTP_RESPONSE')
            :param uri : the url to contact
            :param params : dict or already encoded parameters for the request to make
            :param headers : headers of request
            :param method : the method to use to make the request
            :param preuri : pre url to prepend to param uri.
            :param timeout : timeout for the request in seconds
        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        _log_params = (params or {}).copy()
        _logger.debug("Uri: %s - Type : %s - Headers: %s - Params : %s!",
                      uri, method, headers, _log_params)

        ask_time = fields.Datetime.now()
        try:
            if method.upper() in ('GET', 'DELETE'):
                res = requests.request(
                    method.lower(), preuri + uri, params=params, timeout=timeout)
            elif method.upper() in ('POST', 'PATCH', 'PUT'):
                res = requests.request(
                    method.lower(), preuri + uri, data=params, headers=headers, timeout=timeout)
            else:
                raise Exception(
                    _('Method not supported [%s] not in [GET, POST, PUT, PATCH or DELETE]!', method))
            res.raise_for_status()
            status = res.status_code

            if int(status) == 204:  # No content
                response = False
            else:
                response = res.json()

            try:
                ask_time = datetime.strptime(res.headers.get(
                    'date', ''), "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                pass
        except requests.HTTPError as error:
            if error.response.status_code in (204, 404):
                status = error.response.status_code
                response = ""
            else:
                _logger.exception("Bad %s request : %s!" %
                                  (self._service_name, error.response.content))
                raise error
        return (status, response, ask_time)

    def _get_client_secret(self):
        ICP = self.env['ir.config_parameter'].sudo()
        return ICP.get_param('%s_client_secret' % self._service_name)

    def _get_client_id(self):
        ICP = self.env['ir.config_parameter'].sudo()
        return ICP.get_param('%s_client_id' % self._service_name)

    @api.model
    def _get_authorize_uri(self, scope, redirect_uri, state=None, approval_prompt=None, access_type=None):
        """ This method return the url needed to allow this instance of Odoo to access to the scope
            of gmail specified as parameters
        """
        params = {
            'response_type': 'code',
            'client_id': self._get_client_id(),
            'scope': scope,
            'redirect_uri': redirect_uri,
        }

        if state:
            params['state'] = state

        if approval_prompt:
            params['approval_prompt'] = approval_prompt

        if access_type:
            params['access_type'] = access_type

        encoded_params = urls.url_encode(params)
        return "%s?%s" % (self._service_auth_endpoint, encoded_params)

    @api.model
    def _get_tokens(self, authorize_code,scope,  redirect_uri):
        return
    def _refresh_token(self, rtoken):
        return
    
