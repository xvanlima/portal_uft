from collections import defaultdict
from plone.restapi.services import Service


class RosterGET(Service):
    """Return a roster of Persons in a Campus"""

    def replay(self):
        campus = self.context
        persons = campus.persons()
        result = defaultdict(list)
        for person in persons:
            person_id = person.id
            result[person_id]
            result[person_id]
        return result
