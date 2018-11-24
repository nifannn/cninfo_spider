from .base import StatementSpider

URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1076'

class CashFlowStatementSpider(StatementSpider):
	"""docstring for CashFlowStatementSpider"""
	def __init__(self, sheet_type):
		super(CashFlowStatementSpider, self).__init__(sheet_type)
		self.URL = URL
