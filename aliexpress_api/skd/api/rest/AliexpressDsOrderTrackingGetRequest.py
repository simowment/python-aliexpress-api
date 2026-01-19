"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressDsOrderTrackingGetRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.ae_order_id = None
        self.language = None
        self.app_signature = None

    def getapiname(self):
        return "aliexpress.ds.order.tracking.get"
