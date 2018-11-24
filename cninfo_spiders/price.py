from .base import TypeTableSpider

URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1072'

class PriceSpider(TypeTableSpider):
	"""docstring for PriceSpider"""
	def __init__(self, duration_type):
		super(PriceSpider, self).__init__(duration_type)
		self.URL = URL
		self.fields = {
			'F002N' : 'Close',
			'F003N' : 'Open',
			'F004N' : 'Vol',
			'F005N' : 'High',
			'F006N' : 'Low',
			'F010N' : 'Chg',
			'TRADEDATE' : 'Trade_Date'
		}
