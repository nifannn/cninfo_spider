import time
import requests
import numpy as np
import pandas as pd
import logging
 

class BaseSpider(object):
	"""docstring for BaseSpider"""
	def __init__(self):
		self._records = []
		self._config_logging()
		self.USER_AGENT_LIST = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
		self.HEADER = {
    					'Origin': 'http://webapi.cninfo.com.cn',
    					'Referer': 'http://webapi.cninfo.com.cn/', 
    					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    					'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'}

	def __len__(self):
		return len(self._records)

	def _update_user_agent(self, new_user_agent=None):
		if new_user_agent is None:
			self.HEADER['User-Agent'] = np.random.choice(self.USER_AGENT_LIST)
		else:
			self.HEADER['User-Agent'] = new_user_agent

	def _sleep(self, sleep_time=None):
		if sleep_time is None:
			time.sleep(np.clip(np.random.normal(5, 2), 1, 9))
		else:
			time.sleep(sleep_time)

	def _get_time(self):
		return time.strftime('%Y-%m-%d %H:%M:%S')

	def _config_logging(self):
		logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s',
							datefmt='%Y-%m-%d %H:%M:%S',
							level=logging.INFO)

	def _log_info(self, info):
		logging.info(info)

	def _log_warning(self, warning):
		logging.warning(warning)

	def is_empty(self):
		return not bool(self._records)

	def to_df(self):
		return pd.DataFrame(self._records)

	def to_csv(self, path, mode='w'):
		self.to_df().to_csv(path, index=False, mode=mode)

	def to_sql(self):
		pass

	def save(self, path=None, mode='w', to_sql=False, show_info=True):
		if to_sql:
			self.to_sql()
		elif path is None:
			self._log_warning('Saving failed. Please provide a valid filepath.')
			exit()
		if not (path is None):
			self.to_csv(path, mode=mode)
			if show_info:
				self._log_info('Saved in {}.'.format(path))

	def reset(self):
		self._records = []

	@property
	def records(self):
		return self._records
	

class CompanySpider(BaseSpider):
	"""docstring for CompanySpider"""
	def __init__(self):
		super(CompanySpider, self).__init__()
		self.URL = ''
		self._company_code_list = self._get_company_code_list()
		self._company_codes = self._get_company_codes()
		self.fields = dict()

	def _make_request(self, post_data, user_agent=None, max_conn=10):
		self._update_user_agent(user_agent)

		success = False
		fail_number = 0

		while not success:
			try:
				res = requests.post(self.URL, data=post_data, headers=self.HEADER)
				success = True
			except Exception as e:
				fail_number += 1
				self._log_info('Connection failed. Try again.')
				self._sleep(60 * fail_number)

				if fail_number > max_conn:
					raise e
		
		return res.json().get('records', [dict()])

	def _get_company_code_list(self):
		url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1067"
		res = requests.post(url, headers=self.HEADER).json()['records']
		return res

	def _get_company_codes(self):
		return {rec['SECCODE'] : rec['SECNAME'] for rec in self._company_code_list}

	def _add_basic_info(self, record, seccode):
		record['Sec_Code'] = seccode
		record['Sec_Name'] = self._company_codes[seccode]
		record['Record_Time'] = self._get_time()
		record['Source'] = self.URL
		return record

	def _naive_parse(self, record, seccode):
		process_val = lambda val: '' if val is None else val
		new_record = {self.fields.get(k, k) : process_val(v) 
					   for k, v in record.items()}
		new_record = self._add_basic_info(new_record, seccode)
		return new_record

	def _naive_parse_many(self, records, seccode):
		return [self._naive_parse(record, seccode) for record in records]


class TableSpider(CompanySpider):
	"""docstring for TableSpider"""
	def __init__(self):
		super(TableSpider, self).__init__()

	def _get_post_data(self, scode):
		return {'scode' : scode}

	def _parse(self, res, scode):
		return self._naive_parse_many(res, scode)

	def _crawl(self, scode):
		if isinstance(scode, int) and len(str(scode)) < 6:
			scode = '0' * (6 - len(str(scode))) + str(scode)
		post_data = self._get_post_data(scode)
		res = self._make_request(post_data)
		return self._parse(res, scode)

	def crawl(self, scodes, reset=False, debug=False, show_info=True):
		if reset:
			self.reset()
		if show_info:
			self._log_info('Crawling ...')

		for idx, scode in enumerate(scodes):
			if debug:
				self._log_info('SECCODE: {}, NAME: {}, NUMBER: {}'.format(scode, self._company_codes[str(scode)], idx))
			self._records += self._crawl(scode)

		if show_info:
			self._log_info('Done.')

		return self

	def crawl_and_save(self, scodes, path, reset=False, debug=False, show_info=True, save_iter=100):
		if reset:
			self.reset()

		if show_info:
			self._log_info('Crawling ...')

		for idx, scode in enumerate(scodes):
			if debug:
				self._log_info('Number: {}, Seccode: {}, Name: {}'.format(idx+1, scode, self._company_codes[str(scode)]))
			self._records += self._crawl(scode)

			if (idx+1) % save_iter == 0:
				self.save(path, mode='a', show_info=show_info)
				self.reset()

		if not self.is_empty():
			self.save(path, mode='a', show_info=show_info)

		if show_info:
			self._log_info('Done.')

	def crawl_all(self, debug=False, show_info=True):
		scodes = list(self._company_codes.keys())
		return self.crawl(scodes, reset=True, debug=debug, show_info=show_info)

	def crawl_all_and_save(self, path, debug=False, show_info=True):
		scodes = list(self._company_codes.keys())
		self.crawl_and_save(scodes, path, reset=True, debug=debug, show_info=show_info)
		

class TypeTableSpider(TableSpider):
	"""docstring for SheetSpider"""
	def __init__(self, table_type):
		super(TypeTableSpider, self).__init__()
		self._type = table_type

	def _get_post_data(self, scode):
		return { 'scode' : scode, 'rtype' : self._type }

	@property
	def type(self):
		return self._type


class SheetSpider(TypeTableSpider):
	"""docstring for SheetSpider"""
	def __init__(self, sheet_type):
		super(SheetSpider, self).__init__(sheet_type)

	def _parse(self, res, scode):
		return self._parse_many_records(res, scode)

	def _get_item_year_record(self, item, year, value, scode):
		val = '' if value is None else value
		record = {'Item' : item, 'Year' : year, 'Value' : val}
		return self._add_basic_info(record, scode)

	def _parse_one_record(self, record, scode):
		item = record.get('index', '')
		years = sorted(k for k in record.keys() if k != 'index')
		return [self._get_item_year_record(item, y, record[y], scode)
				for y in years]

	def _parse_many_records(self, res, scode):
		records = []
		for record in res:
			records += self._parse_one_record(record, scode)
		return records


class StatementSpider(SheetSpider):
	"""docstring for StatementSpider"""
	def __init__(self, sheet_type):
		super(StatementSpider, self).__init__(sheet_type)
		self._company_signs = self._get_company_signs()

	def _get_company_signs(self):
		return {rec['SECCODE'] : rec['F002N'] for rec in self._company_code_list}

	def _get_post_data(self, scode):
		return {'scode' : scode, 'rtype' : self._type, 'sign' : self._company_signs[str(scode)]}
		
		
	
		