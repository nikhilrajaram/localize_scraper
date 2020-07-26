from src.model.tradeoff import Tradeoff


class Insight:
    def __init__(self, category=None, tradeoff=None, __typename=None):
        self.category = category
        self.tradeoff = tradeoff
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Insight()

        if type(json) is list:
            return [Insight.from_json(insights) for insights in json]

        return Insight(json.get('category'), Tradeoff.from_json(json.get('tradeoff')), json.get('__typename'))
