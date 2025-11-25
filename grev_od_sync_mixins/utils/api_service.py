# -*- coding: utf-8 -*-

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


        