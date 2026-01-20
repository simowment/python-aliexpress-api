"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressDsFreightQueryRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.query_delivery_req = None
        self.locale = None
        self.app_signature = None

    def getapiname(self):
        return "aliexpress.ds.freight.query"

    def getTranslateParas(self):
        return {"query_delivery_req": "queryDeliveryReq"}
