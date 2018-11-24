from .top_shareholder import ShareholderSpider


URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1071'

class TradableShareholderSpider(ShareholderSpider):
	"""docstring for TradableShareholderSpider"""
	def __init__(self):
		super(TradableShareholderSpider, self).__init__()
		self.URL = URL
