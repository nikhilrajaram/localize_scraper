class EventsHistory:
    def __init__(self, event_type=None, price=None, date=None, __typename=None):
        self.event_type = event_type
        self.price = price
        self.date = date
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return EventsHistory()

        if type(json) is list:
            return [EventsHistory.from_json(eventsHistory) for eventsHistory in json]

        return EventsHistory(json.get('eventType'), json.get('price'), json.get('date'), json.get('__typename'))
