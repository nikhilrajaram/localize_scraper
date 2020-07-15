from src.model.cursor import Cursor
from src.model.poi import Poi


class SearchPoiV2:
    def __init__(self, total=None, cursor=None, total_nearby=None, last_in_geometry_id=None, poi=[], __typename=None):
        self.total = total
        self.cursor = cursor
        self.total_nearby = total_nearby
        self.last_in_geometry_id = last_in_geometry_id
        self.poi = poi
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return SearchPoiV2()

        if type(json) is list:
            return [SearchPoiV2.from_json(searchPoiV2) for searchPoiV2 in json]

        try:
            poi = [Poi.from_json(_poi) for _poi in json.get('poi')]
        except TypeError:
            poi = []

        return SearchPoiV2(json.get('total'), Cursor.from_json(json.get('cursor')), json.get('totalNearby'),
                           json.get('lastInGeometryId'), poi, json.get('__typename'))
