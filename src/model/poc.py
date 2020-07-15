class Poc:
    def __init__(self, type=None, __typename=None):
        self.type = type
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Poc()

        if type(json) is list:
            return [Poc.from_json(poc) for poc in json]

        return Poc(json.get('type'), json.get('__typename'))
