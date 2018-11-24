from .base import StatementSpider

URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1077'

class BalanceSheetSpider(StatementSpider):
	"""docstring for BalanceSheetSpider"""
	def __init__(self, sheet_type):
		super(BalanceSheetSpider, self).__init__(sheet_type)
		self.URL = URL
