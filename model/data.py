from model.searchPoiV2 import SearchPoiV2


class Data:
    def __init__(self, search_poi_v2=None):
        self.search_poi_v2 = search_poi_v2

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Data()

        if type(json) is list:
            return [Data.from_json(data) for data in json]

        return Data(SearchPoiV2.from_json(json.get('searchPoiV2')))
