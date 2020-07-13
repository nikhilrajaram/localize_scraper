from src.model.addressDetails import AddressDetails
from src.model.apiResponsePayload import ApiResponsePayload
from src.model.cursor import Cursor
from src.model.data import Data
from src.model.eventsHistory import EventsHistory
from src.model.images import Images
from src.model.insights import Insights
from src.model.locationPoint import LocationPoint
from src.model.poc import Poc
from src.model.poi import Poi
from src.model.searchPoiV2 import SearchPoiV2
from src.model.status import Status
from src.model.tags import Tags

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
    DEFAULT_QUERY = "query searchPoi($dealType: String, $userContext: JSONObject, $abtests: JSONObject, " \
                    "$noFee: Boolean, $priceRange: [Int], $ppmRange: [Int], $monthlyTaxRange: [Int], $roomsRange: [" \
                    "Int], $bathsRange: [Float], $buildingClass: [String], $amenities: inputAmenitiesFilter, " \
                    "$openHouse: String, $generalCondition: [GeneralCondition], $sellerType: [SellerType], " \
                    "$floorRange: [Int], $areaRange: [Int], $tileRanges: [TileRange], $tileRangesExcl: [TileRange], " \
                    "$sort: [SortField], $limit: Int, $offset: Int, $cursor: inputCursor, $poiTypes: [PoiType], " \
                    "$locationDocId: String, $abtests: JSONObject, $searchContext: SearchContext) {\n  searchPoiV2(" \
                    "noFee: $noFee, dealType: $dealType, userContext: $userContext, abtests: $abtests, priceRange: " \
                    "$priceRange, ppmRange: $ppmRange, monthlyTaxRange: $monthlyTaxRange, roomsRange: $roomsRange, " \
                    "bathsRange: $bathsRange, buildingClass: $buildingClass, sellerType: $sellerType, floorRange: " \
                    "$floorRange, areaRange: $areaRange, generalCondition: $generalCondition, amenities: $amenities, " \
                    "openHouse: $openHouse, tileRanges: $tileRanges, tileRangesExcl: $tileRangesExcl, sort: $sort, " \
                    "limit: $limit, offset: $offset, cursor: $cursor, poiTypes: $poiTypes, locationDocId: " \
                    "$locationDocId, abtests: $abtests, searchContext: $searchContext) {\n    total\n    cursor {\n   " \
                    "   bulletinsOffset\n      projectsOffset\n      seenProjects\n      __typename\n    }\n    " \
                    "totalNearby\n    lastInGeometryId\n    cursor {\n      bulletinsOffset\n      projectsOffset\n   " \
                    "   __typename\n    }\n    ...PoiFragment\n    __typename\n  }\n}\n\nfragment PoiFragment on " \
                    "PoiSearchResult {\n  poi {\n    ...PoiInner\n    ... on Bulletin {\n      rentalBrokerFee\n      " \
                    "eventsHistory {\n        eventType\n        price\n        date\n        __typename\n      }\n   " \
                    "   openHouses {\n        from\n        to\n        __typename\n      }\n      insights {\n       " \
                    " insights {\n          category\n          tradeoff {\n            insightPlace\n            " \
                    "value\n            tagLine\n            impactful\n            __typename\n          }\n         " \
                    " __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  " \
                    "}\n  __typename\n}\n\nfragment PoiInner on Poi {\n  id\n  locationPoint {\n    lat\n    lng\n    " \
                    "__typename\n  }\n  type\n  firstTimeSeen\n  addressDetails {\n    docId\n    city\n    borough\n " \
                    "   zipcode\n    streetName\n    neighbourhood\n    neighbourhoodDocId\n    cityDocId\n    " \
                    "resolutionPreferences\n    streetNumber\n    unitNumber\n    district\n    __typename\n  }\n  " \
                    "... on Project {\n    dealType\n    bedsRange {\n      min\n      max\n      __typename\n    }\n " \
                    "   priceRange {\n      min\n      max\n      __typename\n    }\n    images {\n      path\n      " \
                    "__typename\n    }\n    promotionStatus {\n      status\n      __typename\n    }\n    " \
                    "projectName\n    projectLogo\n    projectMessages {\n      listingDescription\n      " \
                    "__typename\n    }\n    previewImage {\n      path\n      __typename\n    }\n    developers {\n   " \
                    "   id\n      logoPath\n      __typename\n    }\n    tags {\n      bestSchool\n      " \
                    "bestSecular\n      bestReligious\n      safety\n      parkAccess\n      quietStreet\n      " \
                    "bikeFriendly\n      dogPark\n      naturalLight\n      familyFriendly\n      lightRail\n      " \
                    "commute\n      __typename\n    }\n    buildingStage\n    blockDetails {\n      buildingsNum\n    " \
                    "  floorRange {\n        min\n        max\n        __typename\n      }\n      units\n      " \
                    "mishtakenPrice\n      urbanRenewal\n      __typename\n    }\n    __typename\n  }\n  ... on " \
                    "Bulletin {\n    dealType\n    address\n    matchScore\n    beds\n    baths\n    buildingYear\n   " \
                    " area\n    price\n    virtualTours\n    rentalBrokerFee\n    eventsHistory {\n      eventType\n  " \
                    "    price\n      date\n      __typename\n    }\n    status {\n      promoted\n      __typename\n " \
                    "   }\n    poc {\n      type\n      ... on BulletinAgent {\n        officeContact {\n          " \
                    "imageUrl\n          __typename\n        }\n        exclusivity {\n          exclusive\n          " \
                    "__typename\n        }\n        __typename\n      }\n      __typename\n    }\n    tags {\n      " \
                    "bestSchool\n      bestSecular\n      bestReligious\n      safety\n      parkAccess\n      " \
                    "quietStreet\n      bikeFriendly\n      dogPark\n      naturalLight\n      familyFriendly\n      " \
                    "lightRail\n      commute\n      __typename\n    }\n    openHouses {\n      from\n      to\n      " \
                    "__typename\n    }\n    commuteTime\n    dogsParkWalkTime\n    parkWalkTime\n    buildingClass\n  " \
                    "  images {\n      ...ImageItem\n      __typename\n    }\n    __typename\n  }\n  ... on Ad {\n    " \
                    "addressDetails {\n      docId\n      city\n      borough\n      zipcode\n      streetName\n      " \
                    "neighbourhood\n      neighbourhoodDocId\n      resolutionPreferences\n      streetNumber\n      " \
                    "unitNumber\n      __typename\n    }\n    city\n    district\n    firstTimeSeen\n    id\n    " \
                    "locationPoint {\n      lat\n      lng\n      __typename\n    }\n    neighbourhood\n    type\n    " \
                    "__typename\n  }\n  __typename\n}\n\nfragment ImageItem on ImageItem {\n  description\n  " \
                    "imageUrl\n  isFloorplan\n  rotation\n  __typename\n}\n "
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
    RESPONSE_MAP = {
        'data': Data,
        'searchPoiV2': SearchPoiV2,
        'cursor': Cursor,
        'poi': Poi,
        'locationPoint': LocationPoint,
        'addressDetails': AddressDetails,
        'eventsHistory': EventsHistory,
        'status': Status,
        'poc': Poc,
        'tags': Tags,
        'images': Images,
        'insights': Insights
    }

    def __init__(self, no_fee=False, deal_type="unitRent", rooms_range=(3, 3), baths_range=(None, None),
                 floor_range=(None, None), area_range=(None, None), building_class=(), seller_type=(),
                 general_condition=(), ppm_range=(), price_range=(None, None), monthly_tax_range=(None, None),
                 amenities={}, sort=None, open_house=None, commute_coordinates=(None, None), priorities=(),
                 poi_types=("bulletin", "project"), search_context="marketplace", abtests={}, offset=0, limit=1000,
                 query=None):
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

    @staticmethod
    def serialize_response(resp):
        for k, v in resp.items():
            if type(v) is dict:
                try:
                    return SearchPoiRequest.RESPONSE_MAP[k](**SearchPoiRequest.camelcase_dict(v))
                except KeyError:
                    return v
            elif type(v) is list and v:
                try:
                    return [SearchPoiRequest.RESPONSE_MAP[k](**SearchPoiRequest.camelcase_dict(x)) for x in v]
                except KeyError:
                    return v
            else:
                return v

    def get_response(self):
        response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
        if response.status_code != 200:
            raise ValueError

        return response.json()
