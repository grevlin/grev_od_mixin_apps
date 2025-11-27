# -*- coding: utf-8 -*-
"""
API Service Helper

Reusable HTTP wrapper for Odoo connector modules.
Provides authentication, request helpers, endpoint registration,
and unified error handling.

Usage:
    api = APIService(
        base_url="https://api.example.com",
        token="xyz",
    )

    response = api.get("/products", params={"active": True})
"""

from uuid import uuid4
import requests
import json
import logging

from odoo import fields
from odoo.exceptions import UserError
from .helpers import after_commit, needed_token, requires_auth_token


_logger = logging.getLogger(__name__)


class ApiService(object):
    def __init__(self, client):
        self.client = client
        self.api_base_url = client._api_base_url
