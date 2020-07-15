class Tags:
    def __init__(self, best_school=None, best_secular=None, best_religious=None, safety=None, park_access=None,
                 quiet_street=None, bike_friendly=None, dog_park=None, natural_light=None, family_friendly=None,
                 light_rail=None, commute=None, __typename=None):
        self.best_school = best_school
        self.best_secular = best_secular
        self.best_religious = best_religious
        self.safety = safety
        self.park_access = park_access
        self.quiet_street = quiet_street
        self.bike_friendly = bike_friendly
        self.dog_park = dog_park
        self.natural_light = natural_light
        self.family_friendly = family_friendly
        self.light_rail = light_rail
        self.commute = commute
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Tags()

        if type(json) is list:
            return [Tags.from_json(tags) for tags in json]

        return Tags(json.get('bestSchool'), json.get('bestSecular'), json.get('bestReligious'), json.get('safety'),
                    json.get('parkAccess'), json.get('quietStreet'), json.get('bikeFriendly'), json.get('dogPark'),
                    json.get('naturalLight'), json.get('familyFriendly'), json.get('lightRail'), json.get('commute'),
                    json.get('__typename'))
