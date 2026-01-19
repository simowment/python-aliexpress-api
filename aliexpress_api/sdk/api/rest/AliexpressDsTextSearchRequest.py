"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressDsTextSearchRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.keyWord = None
        self.local = None
        self.countryCode = None
        self.categoryId = None
        self.sortBy = None
        self.pageSize = None
        self.pageIndex = None
        self.currency = None
        self.searchExtend = None

    def getapiname(self):
        return "aliexpress.ds.text.search"
