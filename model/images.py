class Images:
    def __init__(self, description=None, image_url=None, is_floorplan=None, rotation=None, __typename=None):
        self.description = description
        self.image_url = image_url
        self.is_floorplan = is_floorplan
        self.rotation = rotation
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Images()

        if type(json) is list:
            return [Images.from_json(images) for images in json]

        return Images(json.get('description'), json.get('imageUrl'), json.get('isFloorplan'), json.get('rotation'),
                      json.get('__typename'))
