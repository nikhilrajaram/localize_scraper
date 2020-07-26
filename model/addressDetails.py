class AddressDetails:
    def __init__(self, doc_id=None, city=None, borough=None, zipcode=None, street_name=None, neighbourhood=None,
                 neighbourhood_doc_id=None, city_doc_id=None, resolution_preferences=None, street_number=None,
                 unit_number=None, district=None, __typename=None):
        self.doc_id = doc_id
        self.city = city
        self.borough = borough
        self.zipcode = zipcode
        self.street_name = street_name
        self.neighbourhood = neighbourhood
        self.neighbourhood_doc_id = neighbourhood_doc_id
        self.city_doc_id = city_doc_id
        self.resolution_preferences = resolution_preferences
        self.street_number = street_number
        self.unit_number = unit_number
        self.district = district
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return AddressDetails()

        if type(json) is list:
            return [AddressDetails.from_json(addressDetails) for addressDetails in json]

        return AddressDetails(json.get('docId'), json.get('city'), json.get('borough'), json.get('zipcode'),
                              json.get('streetName'), json.get('neighbourhood'), json.get('neighbourhoodDocId'),
                              json.get('cityDocId'), json.get('resolutionPreferences'), json.get('streetNumber'),
                              json.get('unitNumber'), json.get('district'), json.get('__typename'))
