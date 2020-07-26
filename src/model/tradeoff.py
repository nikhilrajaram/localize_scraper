class Tradeoff:
    def __init__(self, insight_place=None, value=None, tag_line=None, impactful=None, __typename=None):
        self.insight_place = insight_place
        self.value = value
        self.tag_line = tag_line
        self.impactful = impactful
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        return Tradeoff(json.get('insightPlace'), json.get('value'), json.get('tagLine'), json.get('impactful'), json.get('__typename'))
