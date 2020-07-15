class Status:
    def __init__(self, promoted=None, __typename=None):
        self.promoted = promoted
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Status()

        if type(json) is list:
            return [Status.from_json(status) for status in json]

        return Status(json.get('promoted'), json.get('__typename'))
