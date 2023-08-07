import time
import asyncio
import requests_html
from decorators import filter_objects


class WebManager:
	"""
	The session is created
	for every runtime.
	"""
	def __init__(self):
		self._session = None
		try:
			self._session = requests_html.AsyncHTMLSession()
		except (Exception, requests_html.exceptions.RequestException) as exception:
			print(f'Can not establish connection because {exception}')

	async def get_response(self, url: str):
		"""
		Send a request to the server.
		"""
		response = None
		try:
			response = await self._session.get(url)
		except Exception as exception:
			print(f'Error because {exception}')

		time.sleep(1)
		return response

	async def create_tasks(self, urls: list[str], list_of_tasks=[]):
		"""
		Go through each link and make a request.
		Put each request to the tasks list.
		"""
		for i in range(0, len(urls)):
			time.sleep(1)
			task = asyncio.create_task(self.get_response(urls[i]))
			list_of_tasks.append(task)
		results = await asyncio.gather(*list_of_tasks)
		return results


class FileManager:
	"""
	This object either takes a list
	of links and saves them or gets
	the file and retrieves ones from.
	"""
	def __init__(self, filename: str):
		self.filename = filename

	async def save_links(self, list_of_page_links: list[str]):
		"""
		Save the list of parsed links
		to the flat file.
		"""
		try:
			with open(self.filename, mode='a', encoding='utf-8') as f:
				for i in range(0, len(self.list_of_page_links)):
					f.write(f'{self.list_of_page_links[i]}\n')
		except (Exception, TypeError) as error:
			print(f'cannot operate data saving beacause {error}')
		else:
			print(f'the links have been saved to the \'{self.filename}\'.')

	async def pull_out_page_links(self, links=[]) -> list[str]:
		"""
		Take the saved links from the file.
		"""
		try:
			with open(self.filename, mode='r', encoding='utf-8') as f:
				for link in f.readlines():
					links.append(link)

		except (Exception, FileNotFoundError) as error:
			print(f'cannot retrieve links beacause {error}')
		return links


class WebCrawler:
	"""
	This object collects links
	from each page, saves them
	to the hard disk.
	"""

	def __init__(self, filename: str, site_dict: dict):
		self.site_dict = site_dict
		self.web_manager = WebManager()
		self.list_of_page_links = []

	async def crawl_links(self, url) -> list[str]:
		"""
		Fetch all the links dedicated
		to the topic.
		"""
		self.list_of_page_links.append(url)
		response = await self.web_manager.get_response(url)
		next_page_slug = response.html.find(self.site_dict['next_page'], first=True)
		
		if next_page:
			url = self.site_dict['source'][:18] + next_page_slug

			return await self.crawl_links(url)
		else:
			return self.list_of_page_links


class WebScraper:
	"""
	The object takes a list of
	responses and extracts data
	from each one.
	""" 

	def __init__(self, site_dict: dict):
		self.site_dict = site_dict
		self.web_manager = WebManager()
		self.list_of_row_links = []

	async def extract_table_row_link(self, urls: list[str]) -> None:
		"""
		Find a table on the page and
		extract the item links inside
		of it.
		"""
		results = await self.web_manager.create_tasks(urls)
		for i in range(0, len(results)):
			table = results[i].html.find(self.site_dict['table'], first=True)

			for row in table.find(self.site_dict['row']):
				link = row.find(self.site_dict['link'], first=True).attrs['href']
				self.list_of_row_links.append(self.site_dict['source'][:18] + link)

	@filter_objects
	async def extract_data_of_each_item(self, list_of_objs=[]) -> list[dict]:
		"""
		Follow each link and retrieve
		the corresponding data, form
		an object per page and save
		it to the dataset.
		"""
		results = await self.web_manager.create_tasks(self.list_of_row_links)
		for i in range(0, len(results)):
			obj = results[i].html.xpath(self.site_dict['object'], first=True)

			obj = {
				'date': obj.xpath(self.site_dict['date'], first=True),
				'square': obj.xpath(self.site_dict['square'][0], first=True),
				'region': obj.xpath(self.site_dict['region'], first=True),
				'status': obj.xpath(self.site_dict['status'], first=True),
				'submit_deadline': obj.xpath(self.site_dict['submit_deadline'], first=True),
				'contribution': obj.xpath(self.site_dict['contribution'], first=True),
				'organizer': obj.xpath(self.site_dict['organizer'], first=True),
			}
			list_of_objs.append(obj)

		return list_of_objs

