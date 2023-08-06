import time
import asyncio
import requests_html


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


class WebCrawler:
	"""
	This object collects links
	from each page, saves them
	to the hard disk.
	"""

	def __init__(self, site_dict: dict):
		self.site_dict = site_dict
		self.web_manager = WebManager()

	async def crawl_links(self) -> list[str]:
		"""
		Fetch all the links dedicated
		to the topic.
		"""
		...


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

