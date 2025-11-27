import json
import logging

from odoo import http,_
from odoo.http import request

_logger = logging.getLogger(__name__)


class OauthController(http.Controller):

    @http.route("/oauth/<string:api_name>/confirm", type="http", auth="public", methods=["GET"], csrf=False, save_session=False)
    def redirect_oauth(self,api_name, **kw):
        if hasattr(self,f'{api_name}_redirect_oauth'):
            return getattr(self,f'{api_name}_redirect_oauth')(**kw)
        raise NotImplementedError(
            _("must be implemented in the inheriting api_name.")
        )

    @http.route("/oauth/<string:api_name>/start", type="http", auth="user", methods=["GET"], csrf=False)
    def oauth_start(self,api_name, **kw):
        if hasattr(self,f'{api_name}_oauth_start'):
            return getattr(self,f'{api_name}_oauth_start')(**kw)
        raise NotImplementedError(
            _("must be implemented in the inheriting api_name.")
        )

    @http.route("/oauth/<string:api_name>/refresh", type="http", auth="user", methods=["GET"], csrf=False)
    def auth_refresh(self,api_name, **kw):
        if hasattr(self,f'{api_name}_auth_refresh'):
            return getattr(self,f'{api_name}_auth_refresh')(**kw)
        raise NotImplementedError(
            _("must be implemented in the inheriting api_name.")
        )
    @http.route("/oauth/<string:api_name>/revoke", type="http", auth="user", methods=["GET"], csrf=False)
    def oauth_revoke(self,api_name, **kw):
        if hasattr(self,f'{api_name}_oauth_revoke'):
            return getattr(self,f'{api_name}_oauth_revoke')(**kw)
        raise NotImplementedError(
            _("must be implemented in the inheriting api_name.")
        )
