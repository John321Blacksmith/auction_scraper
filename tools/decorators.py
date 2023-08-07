from pydantic import BaseModel, ValidationError


class AuctionModel(BaseModel):
	date: str    # дата
	square: str    # участок
	area: str    # регион
	status: str    # статус
	submit_deadline: str    # срок подачи заявок
	contribution: int    # взнос за участие в аукционе
	organizer: str    # организатор




def filter_objects(func):
	def wrapper(*args, **kwargs):
		objects = func(*args, **kwargs)
		new_list = []
		index = 0
		while index < len(objects):
			try:
				new_list.append(AuctionModel(**objects[index]))
			except ValidationError:
				new_list.append(None)

			index += 1

		return new_list

	return wrapper

