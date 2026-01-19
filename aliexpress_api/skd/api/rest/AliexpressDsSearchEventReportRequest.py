"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressDsSearchEventReportRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.event_list = None
        self.locale = None
        self.web_site = None

    def getapiname(self):
        return "aliexpress.ds.search.event.report"
