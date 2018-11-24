import requests
import os
from .base import BaseSpider


URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1001'
MARKET_URL = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1000'


class StockSpider(BaseSpider):
	"""docstring for StockSpider"""

	def _get_markets(self):
		res = requests.post(MARKET_URL, headers=self.HEADER)
		return {t['MARKET']:t['NAME'] for t in res.json()['records']}

	def _make_request(self, market_code, user_agent=None, max_conn=10):
		self._update_user_agent(user_agent)
		success = False
		fail_times = 0
		payload = {'market': market_code,
				   'letter': ''}

		while not success:
			try:
				res = requests.post(URL, data=payload, headers=self.HEADER)
				success = True
			except Exception as e:
				fail_times += 1
				self._log_info(e)
				self._log_info('Connection failed. Try again.')
				self._sleep(60 * fail_times)

				if fail_times > max_conn:
					raise e
		
		return res.json().get('records', [dict()])

	def _process_one_record(self, record, markets):
		columns = {'MARKET':'Symbol',
		           'SSBK':'Exchange',
		           'SSRQ':'IPO_Date', 
		           'ZQJC':'Company_Name', 
		           'ZQLX':'Type',
		           'SECCODE':'Code' }
		new_record = {columns[col]:val for col, val in record.items() if col != 'PYJC'}
		new_record['Exchange_Name'] = markets[new_record['Exchange']]
		new_record['Record_Time'] = self._get_time()
		new_record['Source'] = URL
		return new_record

	def _process_json(self, json_data, markets):
		return [self._process_one_record(record, markets) for record in json_data]

	def get_company_codes(self, market_code):
		res = self._make_request(market_code)
		return {record['MARKET'] : record['ZQJC'] for record in res}

	def crawl_all(self, reset=True):
		if reset:
			self.reset()
		markets = self._get_markets().items()
		for code, market in markets:
			self._log_info('Crawling {}:{}...'.format(code, market))
			self.crawl(code)
			self._log_info('Done.')
		return self

	def crawl(self, market_code, reset=False):
		if reset:
			self.reset()
		res = self._make_request(market_code)
		markets = self._get_markets()
		self._records += self._process_json(res, markets)
		return self

	def crawl_and_save(self, market_code, path="result.csv", reset=False, mode='w', show_info=True):
		self.crawl(market_code, reset).save(path, mode=mode, show_info=show_info)

	def crawl_all_and_save(self, path="result.csv", separate=False, directory="result", show_info=True):
		markets = self._get_markets().items()
		for code, market in markets:
			if show_info:
				self._log_info('Crawling {}:{}...'.format(code, market))
			
			if separate:
				self.crawl_and_save(code, os.path.join(directory, '{}.csv'.format(code)), reset=True, show_info=show_info)
			else:
				self.crawl_and_save(code, path, reset=True, mode='a', show_info=show_info)