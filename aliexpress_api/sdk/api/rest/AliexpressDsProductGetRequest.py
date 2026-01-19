"""
Created by auto_sdk on 2023.11.27
"""
from ..base import RestApi


class AliexpressDsProductGetRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.ship_to_country = None
        self.product_id = None
        self.target_currency = None
        self.target_language = None
        self.remove_personal_benefit = None
        self.biz_model = None
        self.province_code = None
        self.city_code = None
        self.app_signature = None

    def getapiname(self):
        return "aliexpress.ds.product.get"
