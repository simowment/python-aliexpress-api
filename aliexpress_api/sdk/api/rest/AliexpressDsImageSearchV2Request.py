from ..base import RestApi

class AliexpressDsImageSearchV2Request(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.limit = None
        self.image_file_bytes = None
        self.sort = None
        self.target_currency = None
        self.target_language = None
        self.page_size = None
        self.page_index = None
        self.search_type = None

    def getapiname(self):
        return 'aliexpress.ds.image.searchV2'

    def getMultipartParas(self):
        return ['image_file_bytes']
