import asyncio
import requests_html
from tools.scraping_tools import (WebManager, WebScraper, WebCrawler)

from scraping_data import auction_site


async def start_scraping():
	scraper = WebScraper(auction_site)
	links = await scraper.extract_table_row_link([auction_site['source']])
	objects = await scraper.extract_data_of_each_item()
	for i in range(0, len(objects)):
		for key, value in objects.items():
			print(key + ' ::: ' + str(value))

		print('\n\n\n')
	


if __name__ == '__main__':
	asyncio.run(start_scraping())