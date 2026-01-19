"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressLogisticsBuyerFreightCalculateRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.country_code = None
        self.locale = None
        self.product_list = None
        self.web_site = None

    def getapiname(self):
        return "aliexpress.logistics.buyer.freight.calculate"
