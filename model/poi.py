from model.addressDetails import AddressDetails
from model.eventsHistory import EventsHistory
from model.images import Images
from model.insights import Insights
from model.locationPoint import LocationPoint
from model.poc import Poc
from model.status import Status
from model.tags import Tags


class Poi:
    def __init__(self, id=None, location_point=None, type=None, first_time_seen=None, address_details=None,
                 deal_type=None, address=None, match_score=None, beds=None, baths=None, building_year=None, area=None,
                 price=None, virtual_tours=None, rental_broker_fee=None, events_history=[], status=None, poc=None,
                 tags=None, open_houses=[], commute_time=None, dogs_park_walk_time=None, park_walk_time=None,
                 building_class=None, images=[], __typename=None, insights=None):
        self.id = id
        self.location_point = location_point
        self.type = type
        self.first_time_seen = first_time_seen
        self.address_details = address_details
        self.deal_type = deal_type
        self.address = address
        self.match_score = match_score
        self.beds = beds
        self.baths = baths
        self.building_year = building_year
        self.area = area
        self.price = price
        self.virtual_tours = virtual_tours
        self.rental_broker_fee = rental_broker_fee
        self.events_history = events_history
        self.status = status
        self.poc = poc
        self.tags = tags
        self.open_houses = open_houses
        self.commute_time = commute_time
        self.dogs_park_walk_time = dogs_park_walk_time
        self.park_walk_time = park_walk_time
        self.building_class = building_class
        self.images = images
        self.__typename = __typename
        self.insights = insights

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Poi()

        if type(json) is list:
            return [Poi.from_json(poi) for poi in json]

        try:
            eventsHistory = [EventsHistory.from_json(_eventsHistory) for _eventsHistory in json.get('eventsHistory')]
        except TypeError:
            eventsHistory = []

        try:
            images = [Images.from_json(_images) for _images in json.get('images')]
        except TypeError:
            images = []

        return Poi(json.get('id'), LocationPoint.from_json(json.get('locationPoint')), json.get('type'),
                   json.get('firstTimeSeen'), AddressDetails.from_json(json.get('addressDetails')),
                   json.get('dealType'), json.get('address'), json.get('matchScore'), json.get('beds'),
                   json.get('baths'), json.get('buildingYear'), json.get('area'), json.get('price'),
                   json.get('virtualTours'), json.get('rentalBrokerFee'), eventsHistory,
                   Status.from_json(json.get('status')), Poc.from_json(json.get('poc')),
                   Tags.from_json(json.get('tags')), json.get('openHouses'), json.get('commuteTime'),
                   json.get('dogsParkWalkTime'), json.get('parkWalkTime'), json.get('buildingClass'), images,
                   json.get('__typename'), Insights.from_json(json.get('insights')))
