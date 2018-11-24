import requests
from .base import BaseSpider


URL = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1068"

class CompanyInfoSpider(BaseSpider):
	"""docstring for CompanyInfoSpider"""
	def __init__(self):
		super(CompanyInfoSpider, self).__init__()
		self.URL = URL
		self._company_records = self._get_company_records()
		self.fields = {
			'F001D': 'Founded',
			'F002D': 'Listing',
			'F003V': 'Website', 
			'F004V': 'Domicile',
			'F005V': 'Office',
			'F006V': 'Email',
			'F007V': 'Telephone',
			'F008V': 'Fax',
			'F009V': 'CSRC_Sector',
			'F010V': 'CSRC_Subsector',
			'F011V': 'Market',
			'F012V': 'Company_Business',
			'F013V': 'Business_Scope',
			'ORGNAME': 'Org_Name',
			'SECCODE': 'Sec_Code',
			'SECNAME': 'Sec_Name'
		}

	def _make_request(self, user_agent=None, max_conn=10):
		self._update_user_agent(user_agent)
		success = False
		fail_times = 0

		while not success:
			try:
				res = requests.post(self.URL, headers=self.HEADER)
				success = True
			except Exception as e:
				fail_times += 1
				self._log_info(e)
				self._log_info('Connection failed. Try again.')
				self._sleep(60 * fail_times)

				if fail_times > max_conn:
					raise e
		
		return res.json().get('records', [dict()])

	def _get_company_records(self):
		records = self._make_request()
		return {d['SECCODE'] : d for d in records}

	def _parse_one_record(self, record):
		get_key = lambda key : self.fields.get(key, key)
		get_val = lambda val : '' if val is None else val

		new_record = {get_key(key) : get_val(val) for key, val in record.items()}
		new_record['Record_Time'] = self._get_time()
		new_record['Source'] = URL
		return new_record

	def _parse_records(self, records):
		return [self._parse_one_record(record) for record in records]

	def _extract_record(self, scode):
		code = scode if isinstance(scode, str) and len(scode) == 6 else '0' * (6-len(str(scode))) + str(scode)
		return self._company_records.get(code, dict())

	def crawl(self, scodes, reset=False):
		if reset:
			self.reset()

		records = [self._extract_record(code) for code in scodes]
		self._records += self._parse_records(records)
		return self

	def crawl_and_save(self, scodes, path, reset=False, show_info=True):
		self.crawl(scodes, reset=reset).save(path, show_info=show_info)

	def crawl_all(self):
		self.reset()
		self._records += self._parse_records(self._company_records.values())
		return self

	def crawl_all_and_save(self, path, show_info=True):
		self.crawl_all().save(path, show_info=show_info)