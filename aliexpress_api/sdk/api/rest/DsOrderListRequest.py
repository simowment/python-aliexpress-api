"""
Created by auto_sdk on 2026.02.06
"""
from ..base import RestApi


class DsOrderListRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.start_time = None
        self.end_time = None
        self.status = None
        self.fields = None
        self.locale = None
        self.page_no = None
        self.page_size = None
        self.app_signature = None

    def getapiname(self):
        return "aliexpress.ds.order.list"
