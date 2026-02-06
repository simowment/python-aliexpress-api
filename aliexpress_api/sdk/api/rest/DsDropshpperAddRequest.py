"""
Created by auto_sdk on 2026.02.06
"""
from ..base import RestApi


class DsDropshpperAddRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_name = None
        self.country = None
        self.email = None
        self.locale = None
        self.mobile = None
        self.platform = None
        self.app_signature = None

    def getapiname(self):
        return "aliexpress.ds.dropshipper.add"
