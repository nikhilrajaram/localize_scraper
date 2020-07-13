class EventsHistory:
    def __init__(self, event_type=None, price=None, date=None, __typename=None):
        self.event_type = event_type
        self.price = price
        self.date = date
        self.__typename = __typename
