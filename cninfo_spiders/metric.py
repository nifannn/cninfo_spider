from .base import SheetSpider

URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1074'

class MetricSpider(SheetSpider):
	"""docstring for MetricSpider"""
	def __init__(self, sheet_type):
		super(MetricSpider, self).__init__(sheet_type)
		self.URL = URL
		