class Group:

    def __init__(self, id, areaId):
        self.id = id
        self.areaId = areaId
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def to_dict(self):
        return {
            'id': self.id,
            'areaId': self.areaId,
            'users': [user.to_dict for user in self.users]
        }
