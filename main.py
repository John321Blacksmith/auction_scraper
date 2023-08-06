import time
import asyncio
import requests_html
from tools.data_tools import DataManager
from tools.scraping_tools import (WebManager, WebScraper, WebCrawler, FileManager)

from scraping_data import auction_site


file_manager = FileManager('links.csv')


async def crawl_and_save_pages_links(filename):
	"""
	The first look at the website
	and collecting the links in a
	txt file.
	"""
	crawler = WebCrawler(filename, auction_site)
	# gather links
	await crawler.crawl_links(auction_site['source'])
	# save them
	await file_manager.save_links(crawler.list_of_page_links)
	

async def extract_auctions():
	"""
	Query the file with links
	and use each link for request.
	"""
	# take links out 
	links = await file_manager.pull_out_page_links()

	scraper = WebScraper(auction_site)
	# getting the row links
	row_links = await scraper.extract_table_row_link(links)

	# form auction object from each page
	auctions = await scraper.exctract_data_of_each_item()

	return auctions


async def save_auctions():
	auctions = await extract_auctions()
	data_manager = DataManager()

	
# wait a little bit
time.sleep(3)
if __name__ == '__main__':
	asyncio.run(main())