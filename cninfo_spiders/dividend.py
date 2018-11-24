from .base import TableSpider

URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1073'

class DividendSpider(TableSpider):
	"""docstring for DividendSpider"""
	def __init__(self):
		super(DividendSpider, self).__init__()
		self.URL = URL
		self.fields = {
			'F010N' : 'Cash_div_per_share',
			'F011N' : 'Stock_div_per_share',
			'F012N' : 'Bonus_issue_per_share',
			'F013D' : 'Declaration_date',
			'F014D' : 'Ex_div_date',
			'F015D' : 'Record_date',
			'F016D' : 'Cash_pay_day',
			'F017D' : 'Stock_pay_day'
		}
