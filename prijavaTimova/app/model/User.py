class User:
    def __init__(self, id, name, lastName, year, link, idGroup):
        self.id = id
        self.name = name
        self.lastName = lastName
        self.year = year
        self.link = link
        self.idGroup = idGroup

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastName': self.lastName,
            'year': self.year,
            'link': self.link,
            'idGroup': self.idGroup
        }
