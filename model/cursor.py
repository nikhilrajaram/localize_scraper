class Cursor:
    def __init__(self, bulletins_offset=None, projects_offset=None, seen_projects=[], __typename=None):
        self.bulletins_offset = bulletins_offset
        self.projects_offset = projects_offset
        self.seen_projects = seen_projects
        self.__typename = __typename

    @classmethod
    def from_json(cls, json):
        if json is None:
            return Cursor()

        if type(json) is list:
            return [Cursor.from_json(cursor) for cursor in json]

        return Cursor(json.get('bulletinsOffset'), json.get('projectsOffset'), json.get('seenProjects'),
                      json.get('__typename'))
