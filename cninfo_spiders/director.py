import requests
import numpy as np
from .base import BaseSpider


URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1069'

class DirectorSpider(BaseSpider):
	"""docstring for DirectorSpider"""
	def __init__(self):
		super(DirectorSpider, self).__init__()
		self.URL = URL
		self.company_codes = self._get_company_codes()
		self.fields_en = {
			'F001V': 'Chairman',
			'F002V': 'General_Manager',
			'F003V': 'CFO',
			'F004V': 'Board_Secretary',
			'F005V': 'Board_Members'
		}
		self.fields_cn = {
			'F001V': '董事长',
			'F002V': '总经理',
			'F003V': '财务总监',
			'F004V': '董事会秘书',
			'F005V': '董事会成员'
		}

	def _get_company_codes(self):
		url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1067"
		res = requests.post(url, headers=self.HEADER).json()['records']
		return {rec['SECCODE'] : rec['SECNAME'] for rec in res}

	def _make_request(self, scode, user_agent=None, max_conn=10):
		if user_agent is None:
			self._update_user_agent()
		else:
			self._update_user_agent(user_agent)

		data = {'scode': scode}
		success = False
		fail_number = 0

		while not success:
			try:
				res = requests.post(URL, data=data, headers=self.HEADER)
				success = True
			except Exception as e:
				fail_number += 1
				self._log_info('Connection failed. Try again.')
				self._sleep(60 * fail_number)

				if fail_number > max_conn:
					raise e
		
		return res.json().get('records', [dict()])

	def _add_basic_info(self, record, seccode):
		record['Sec_Code'] = str(seccode)
		record['Sec_Name'] = self.company_codes[str(seccode)]
		record['Record_Time'] = self._get_time()
		record['Source'] = URL
		return record

	def _get_person2title(self, record):
		person2title = dict()
		get_title = lambda p, t: person2title[p] + ',' + t if p in person2title else t
		
		for k, v in record.items():
			if v is not None:
				if k == 'F005V':
					persons = v.split('，')
					for p in persons:
						person2title[p] = get_title(p, self.fields_cn[k])
				else:
					person2title[v] = get_title(v, self.fields_cn[k])
		return person2title

	def _generate_person_record(self, person, title, seccode):
		record = {'Name': person, 'Title': title}
		record = self._add_basic_info(record, seccode)
		return record

	def _raw_parse(self, record, seccode):
		process_val = lambda val: '' if val is None else val
		new_record = {self.fields_en[k]:process_val(v) for k, v in record.items()}
		new_record = self._add_basic_info(new_record, seccode)
		return [new_record]

	def _relation_parse(self, record, seccode):
		person2title = self._get_person2title(record)
		record = [self._generate_person_record(p, t, seccode) for p, t in person2title.items()]
		return record

	def _crawl(self, seccode, relation_parse=False):
		if str(seccode) not in self.company_codes:
			return []

		record = self._make_request(seccode)[0]
		if relation_parse:
			record = self._relation_parse(record, seccode)
		else:
			record = self._raw_parse(record, seccode)
		
		return record

	def crawl_all(self, relation_parse=False, debug=False, show_info=True):
		self.reset()
		if show_info:
			self._log_info('Crawling ...')

		scodes = list(self.company_codes.keys())
		np.random.shuffle(scodes)

		for idx, scode in enumerate(scodes):
			if debug:
				self._log_info('SECCODE: {}, number: {}'.format(scode, idx))
			self._records += self._crawl(scode, relation_parse)
			self._sleep()

			if idx % 15 == 0:
				self._sleep(15)

		if show_info:
			self._log_info('Done.')
		
		return self

	def crawl_all_and_save(self, path, relation_parse=False, debug=False, show_info=True):
		self.crawl_all(relation_parse, debug, show_info).save(path, show_info=show_info)

	def crawl_companies(self, codes, relation_parse=False, reset=False, debug=False, show_info=True):
		if reset:
			self.reset()
		if show_info:
			self._log_info('Crawling ...')

		for idx, scode in enumerate(codes):
			if debug:
				self._log_info('SECCODE: {}, number: {}'.format(scode, idx))
			self._records += self._crawl(scode, relation_parse)
			self._sleep()

			if idx % 20 == 0:
				self._sleep(15)

		if show_info:
			self._log_info('Done.')
		
		return self

	def crawl_companies_and_save(self, codes, path, relation_parse=False,
								 reset=False, debug=False, mode='w', show_info=True):
		self.crawl_companies(codes, relation_parse, reset, debug, show_info).save(path, mode=mode, show_info=show_info)
			
		