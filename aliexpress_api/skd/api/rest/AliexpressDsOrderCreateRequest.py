"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressDsOrderCreateRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.param_place_order_request4_open_api_d_t_o = None
        self.ds_extend_request = None
        self.app_signature = None

    def getapiname(self):
        return "aliexpress.ds.order.create"
