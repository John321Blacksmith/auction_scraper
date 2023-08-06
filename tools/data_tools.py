import asyncio
import psycopg2


class DataManager:
	"""
	This object takes a list of
	items and dumps each one to
	the database.
	"""
	def __init__(self, list_of_objs: list[dict], **creds):
		self.list_ob_objects = list_of_objects
		self._creds = creds


	async def connect_to_db(self, connection=None):
		"""
		Connect to the DB and
		return a connection
		object.
		"""
		connection = psycopg2.connect(**self._creds)
		return connection 

	async def save_records(self, connection) -> None:
		"""
		Save each python object
		as a record to the DB.
		"""
		try:
			connection = await self.connect_to_db()
			cursor = connection.cursor()

			for i in range(0, len(self.list_ob_objects)):
				cursor.execute("""INSERT INTO auctions(date, square, area, status, submit_deadline, contribution, organizer)
								  VALUES(%s,%s,%s,%s,%s,%s,%s);
								""",
					(
						self.list_of_objects[i]['date'],
						self.list_of_objects[i]['square'],
						self.list_of_objects[i]['region'],
						self.list_of_objects[i]['status'],
						self.list_of_objects[i]['submit_deadline'],
						self.list_of_objects[i]['contribution'],
						self.list_of_objects[i]['organizer'],
				)
			)

			connection.commit()

			cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(f'Cannot perform transaction because {error}')

		finally:
			if connection is not None:
				connection.close()

		