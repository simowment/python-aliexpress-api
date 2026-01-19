"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressDsProductGetRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.country = None
        self.fields = None
        self.locale = None
        self.target_currency = None
        self.target_language = None
        self.web_site = None
        self.product_id = None

    def getapiname(self):
        return "aliexpress.ds.product.get"
