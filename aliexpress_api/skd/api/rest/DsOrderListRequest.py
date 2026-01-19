"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class DsOrderListRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.end_time = None
        self.fields = None
        self.locale = None
        self.page_no = None
        self.page_size = None
        self.start_time = None
        self.status = None

    def getapiname(self):
        return "ds.order.list"
