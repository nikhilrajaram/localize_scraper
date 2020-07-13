class Cursor:
    def __init__(self, bulletins_offset=None, projects_offset=None, seen_projects=[], __typename=None):
        self.bulletins_offset = bulletins_offset
        self.projects_offset = projects_offset
        self.seen_projects = seen_projects
        self.__typename = __typename
