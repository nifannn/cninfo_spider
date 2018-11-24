from .base import TableSpider


URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1070'

class ShareholderSpider(TableSpider):
	"""docstring for ShareholderSpider"""
	def __init__(self):
		super(ShareholderSpider, self).__init__()
		self.URL = URL
		self.fields = {
			'F001D' : 'Date',
			'F002V' : 'Name',
			'F003N' : 'Shares(10K)',
			'F004N' : 'Percentage',
			'F005N' : 'Place'
		}