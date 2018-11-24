import sys
import numpy as np

sys.path.append('../')

import cninfo_spiders as cninfo


def generate_random_codes(num):
	spider = cninfo.base.CompanySpider()
	spider._log_info('Preparing data ...')
	spider._log_info('Generating seccodes randomly ...')
	codes = np.random.choice(list(spider._company_codes.keys()), num, replace=False)
	return codes.tolist()

def prepare_company_list(codes):
	spider = cninfo.stock.StockSpider()
	spider._log_info('Preparing company list ...')
	res = spider._make_request('SZE')
	res += spider._make_request('SHE')
	res = [r for r in res if r['MARKET'] in codes]
	markets = spider._get_markets()
	spider._records += spider._process_json(res, markets)
	spider.save('data/company_list.csv', show_info=False)

def prepare_company_info(codes):
	spider = cninfo.company_info.CompanyInfoSpider()
	spider._log_info('Preparing company info ...')
	spider.crawl_and_save(codes, 'data/company_info.csv', reset=True, show_info=False)

def prepare_board_members(codes):
	spider = cninfo.director.DirectorSpider()
	spider._log_info('Preparing board members ...')
	spider.crawl_and_save(codes, 'data/director.csv',
									reset=True, show_info=False)
	spider.crawl_and_save(codes, 'data/relation_director.csv',
									relation_parse=True, reset=True, show_info=False)

def prepare_top_shareholders(codes):
	spider = cninfo.top_shareholder.ShareholderSpider()
	spider._log_info('Preparing top share holders ...')
	spider.crawl_and_save(codes, 'data/top_shareholder.csv', reset=True, show_info=False)

def prepare_top_tradable_shareholders(codes):
	spider = cninfo.top_tradable_shareholder.TradableShareholderSpider()
	spider._log_info('Preparing top tradable share holders ...')
	spider.crawl_and_save(codes, 'data/top_tradable_shareholder.csv', reset=True, show_info=False)

def prepare_dividend(codes):
	spider = cninfo.dividend.DividendSpider()
	spider._log_info('Preparing dividend ...')
	spider.crawl_and_save(codes, 'data/dividend.csv', reset=True, show_info=False)

def prepare_price(codes):
	types = {
		'1' : 'month',
		'2' : '3month',
		'3' : '6month',
		'4' : 'year'
	}

	for t, c in types.items():
		spider = cninfo.price.PriceSpider(t)
		spider._log_info('Preparing recent {} prices ...'.format(c))
		spider.crawl_and_save(codes, 'data/recent_{}_price.csv'.format(c),
							  reset=True, show_info=False)

def prepare_metric(codes):
	types = {
		'1' : 'quarter',
		'2' : 'half_year',
		'3' : 'quarter3',
		'4' : 'year'
	}

	for t, c in types.items():
		spider = cninfo.metric.MetricSpider(t)
		spider._log_info('Preparing {} metrics ...'.format(c))
		spider.crawl_and_save(codes, 'data/{}_metric.csv'.format(c),
			                  reset=True, show_info=False)

def prepare_income(codes):
	types = {
		'1' : 'quarter',
		'2' : 'half_year',
		'3' : 'quarter3',
		'4' : 'year'
	}

	for t, c in types.items():
		spider = cninfo.income.IncomeStatementSpider(t)
		spider._log_info('Preparing {} income statements ...'.format(c))
		spider.crawl_and_save(codes, 'data/{}_income.csv'.format(c),
							  reset=True, show_info=False)

def prepare_balance(codes):
	types = {
		'1' : 'quarter',
		'2' : 'half_year',
		'3' : 'quarter3',
		'4' : 'year'
	}

	for t, c in types.items():
		spider = cninfo.balance.BalanceSheetSpider(t)
		spider._log_info('Preparing {} balance sheets ...'.format(c))
		spider.crawl_and_save(codes, 'data/{}_balance.csv'.format(c),
							  reset=True, show_info=False)

def prepare_cash_flow(codes):
	types = {
		'1' : 'quarter',
		'2' : 'half_year',
		'3' : 'quarter3',
		'4' : 'year'
	}

	for t, c in types.items():
		spider = cninfo.cash_flow.CashFlowStatementSpider(t)
		spider._log_info('Preparing {} cash flow statements ...'.format(c))
		spider.crawl_and_save(codes, 'data/{}_cash_flow.csv'.format(c),
							  reset=True, show_info=False)

def prepare(num):
	codes = generate_random_codes(num)
	prepare_company_list(codes)
	prepare_company_info(codes)
	prepare_board_members(codes)
	prepare_top_shareholders(codes)
	prepare_top_tradable_shareholders(codes)
	prepare_dividend(codes)
	prepare_price(codes)
	prepare_metric(codes)
	prepare_income(codes)
	prepare_balance(codes)
	prepare_cash_flow(codes)


if __name__ == '__main__':
	prepare(10)