import argparse
import cninfo_spiders as cninfo
import os

NAME2SPIDER = {
	'info' : cninfo.company_info.CompanyInfoSpider,
	'director' : cninfo.director.DirectorSpider,
	'shareholder' : cninfo.top_shareholder.ShareholderSpider,
	'tradable_shareholder' : cninfo.top_tradable_shareholder.TradableShareholderSpider,
	'price' : cninfo.price.PriceSpider,
	'dividend' : cninfo.dividend.DividendSpider,
	'metric' : cninfo.metric.MetricSpider,
	'income' : cninfo.income.IncomeStatementSpider,
	'balance' : cninfo.balance.BalanceSheetSpider,
	'cash_flow' : cninfo.cash_flow.CashFlowStatementSpider
}
TYPESPIDERS = ['price', 'metric', 'income', 'balance', 'cash_flow']

def parse_args():
	parser = argparse.ArgumentParser(description="Spiders to crawl cninfo.")
	parser.add_argument('spider_name', type=str, choices=list(NAME2SPIDER.keys()), help="spider name")
	parser.add_argument('file', help="path to save")
	parser.add_argument('-t', default=1, help="sheet type")
	return vars(parser.parse_args())

def run_spider(spider_name, file, t=1):
	if 'out' not in os.listdir():
		os.mkdir('out')
	path = os.path.join('out', file)
	spider = NAME2SPIDER[spider_name]
	if spider_name in TYPESPIDERS:
		s = spider(t)
	else:
		s = spider()
	s.crawl_all_and_save(path)

if __name__ == '__main__':
	args = parse_args()
	run_spider(**args)