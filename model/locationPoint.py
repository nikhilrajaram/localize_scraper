class LocationPoint:
    def __init__(self, lat=None, lng=None, __typename=None):
        self.lat = lat
        self.lng = lng
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return LocationPoint()

        if type(json) is list:
            return [LocationPoint.from_json(locationPoint) for locationPoint in json]

        return LocationPoint(json.get('lat'), json.get('lng'), json.get('__typename'))
