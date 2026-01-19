"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class DsDropshpperAddRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.app_name = None
        self.country = None
        self.email = None
        self.locale = None
        self.mobile = None
        self.platform = None

    def getapiname(self):
        return "ds.dropshpper.add"
