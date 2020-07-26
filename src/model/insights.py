from src.model.insight import Insight


class Insights:
    def __init__(self, insights=[], __typename=None):
        self.insights = insights
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Insights()

        if type(json) is list:
            return [Insights.from_json(insights) for insights in json]

        try:
            insights = [Insight.from_json(_insights) for _insights in json.get('insights')]
        except TypeError:
            insights = []

        return Insights(insights, json.get('__typename'))
