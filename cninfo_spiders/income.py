from .base import StatementSpider

URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1075'

class IncomeStatementSpider(StatementSpider):
	"""docstring for IncomeStatementSpider"""
	def __init__(self, sheet_type):
		super(IncomeStatementSpider, self).__init__(sheet_type)
		self.URL = URL
