from model.data import Data


class ApiResponsePayload:
	def __init__(self, data=None):
		self.data = data

	@classmethod
	def from_json(cls, json):
		if json is None:
			return ApiResponsePayload()

		if type(json) is list:
			return [ApiResponsePayload.from_json(apiResponsePayload) for apiResponsePayload in json]

		return ApiResponsePayload(Data.from_json(json.get('data')))
