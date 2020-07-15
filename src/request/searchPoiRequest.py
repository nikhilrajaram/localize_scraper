from src.model.apiResponsePayload import ApiResponsePayload

import requests
import json
import re


class SearchPoiRequest:
    DEFAULT_DATA = {
        "operationName": "searchPoi",
        "variables": {}
    }
    DEFAULT_SORT = [
        {"field": "naturalLight", "order": "asc"},
        {"field": "safety", "order": "asc"},
        {"field": "parkAccess", "order": "asc"},
        {"field": "commute", "order": "asc"},
    ]
    DEFAULT_USER_CONTEXT = {
        "commutePreference": {
            "location": {
                "lng": None,
                "lat": None
            },
            "text": "",
            "commuteType": "commute",
            "rushHour": False,
            "docId": "",
            "maxCommute": None
        }
    }
    with open('request/payload/query.txt') as f:
        DEFAULT_QUERY = f.read()

    HEADERS = {
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'content-type': 'application/json',
        'accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.116 Safari/537.36 '
    }
    URL = 'https://www.localize.city/api2'

    def __init__(self, no_fee=False, deal_type="unitRent", rooms_range=(None, None), baths_range=(None, None),
                 floor_range=(None, None), area_range=(None, None), building_class=(), seller_type=(),
                 general_condition=(), ppm_range=(), price_range=(None, None), monthly_tax_range=(None, None),
                 amenities=None, sort=None, open_house=None, commute_coordinates=(None, None), priorities=(),
                 poi_types=("bulletin", "project"), search_context="marketplace", abtests=None, offset=0, limit=1000,
                 query=None):
        if abtests is None:
            abtests = {}
        if amenities is None:
            amenities = {}
        self.data = SearchPoiRequest.DEFAULT_DATA
        variables = self.data['variables']
        variables['noFee'] = no_fee
        variables['dealType'] = deal_type
        variables['roomsRange'] = rooms_range
        variables['bathsRange'] = baths_range
        variables['floorRange'] = floor_range
        variables['areaRange'] = area_range
        variables['buildingClass'] = building_class
        variables['sellerType'] = seller_type
        variables['generalCondition'] = general_condition
        variables['ppmRange'] = ppm_range
        variables['priceRange'] = price_range
        variables['monthlyTaxRange'] = monthly_tax_range
        variables['amenities'] = amenities
        variables['sort'] = SearchPoiRequest.DEFAULT_SORT if not sort else sort
        variables['openHouse'] = open_house
        variables['userContext'] = SearchPoiRequest.DEFAULT_USER_CONTEXT
        if commute_coordinates == (None, None):
            del variables['userContext']['commutePreference']
        else:
            variables['userContext']['commutePreference']['location']['lng'], \
                variables['userContext']['commutePreference']['location']['lat'] = commute_coordinates
        if priorities:
            variables['userContext']['priorities'] = priorities
        variables['poiTypes'] = poi_types
        variables['searchContext'] = search_context
        variables['offset'] = offset
        variables['limit'] = limit
        variables['abtests'] = abtests
        self.data['query'] = SearchPoiRequest.DEFAULT_QUERY if not query else query
        self.headers = SearchPoiRequest.HEADERS
        self.url = SearchPoiRequest.URL

    @staticmethod
    def camelcase_to_snaked(s):
        """
        Converts a camelCase string to a string separated by underscores
        credit: https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
        :param s: input string
        :return: underscore separated output
        """
        return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

    @staticmethod
    def camelcase_dict(d):
        new_d = {}
        for k, v in d.items():
            new_d[SearchPoiRequest.camelcase_to_snaked(k)] = v

        return new_d

    def get_response(self):
        response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
        if response.status_code != 200:
            raise ValueError

        return ApiResponsePayload.from_json(response.json())
