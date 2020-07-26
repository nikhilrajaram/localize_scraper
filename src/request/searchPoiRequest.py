from src.model.apiResponsePayload import ApiResponsePayload

import requests
import asyncio
import aiohttp
import json
import re
import numpy as np
from copy import deepcopy


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
        self._sync_session = requests.Session()
        self._async_session = None

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
        """
        Returns a dictionary with all keys camelCased
        :param d: dictionary to camelCase
        :return: camelCased key dictionary
        """
        new_d = {}
        for k, v in d.items():
            new_d[SearchPoiRequest.camelcase_to_snaked(k)] = v

        return new_d

    async def _async_session_init(self):
        """
        Instantiate asynchronous connection pool
        :return: None
        """
        self._async_session = aiohttp.ClientSession()

    def _execute_sync(self):
        """
        Execute a synchronous request to the Localize API
        :return: json-like response body as a dict
        """
        response = self._sync_session.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
        if response.status_code != 200:
            raise ValueError

        return response.json()

    async def _execute_async(self, payload):
        """
        Create a coroutine for a single request to the Localize API
        :param payload: payload to POST
        :return: request coroutine
        """
        async with self._async_session.post(url=self.url, headers=self.headers, data=json.dumps(payload)) as response:
            if response.status != 200:
                raise ValueError

            return await response.json()

    async def _batch_execute_async(self, payloads):
        """
        Asynchronously perform requests to Localize API to list of payloads
        :param payloads: list of payloads to POST
        :return: list of responses
        """
        tasks = [self._execute_async(payload) for payload in payloads]
        resps = await asyncio.gather(self._async_session_init(), *tasks, return_exceptions=True)
        await self._async_session.close()
        return resps

    def execute(self):
        """
        Execute request
        If request is paginated, make requests asynchronously
        Serialize response and return
        :return: Serialized response
        """
        page = 0
        response = ApiResponsePayload.from_json(self._execute_sync())
        total_len = response.data.search_poi_v2.total
        response_len = len(response.data.search_poi_v2.poi)
        payloads = []
        for i in range(1, np.ceil(total_len / response_len).astype(int)):
            page += 1
            payload = deepcopy(self.data)
            payload['variables']['offset'] += response_len
            payloads.append(payload)

        if payloads:
            responses = asyncio.run(self._batch_execute_async(payloads), debug=True)
            for resp in responses:
                if resp is None:
                    continue

                next_page_response = ApiResponsePayload.from_json(resp)
                response.data.search_poi_v2.poi.extend(next_page_response.data.search_poi_v2.poi)

        return response
