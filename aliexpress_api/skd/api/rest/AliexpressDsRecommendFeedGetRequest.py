"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressDsRecommendFeedGetRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.country = None
        self.fields = None
        self.feed_name = None
        self.locale = None
        self.page_no = None
        self.page_size = None
        self.target_currency = None
        self.target_language = None
        self.web_site = None

    def getapiname(self):
        return "aliexpress.ds.recommend.feed.get"
