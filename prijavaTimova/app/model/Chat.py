class Chat:
    def __init__(self, textC, category, idGroup, idUser):
        self.textC = textC
        self.category = category
        self.idUser = idUser
        self.idGroup = idGroup

    def to_dict(self):
        return {
            'textC': self.textC,
            'category': self.category,
            'idUser': self.idUser,
            'idGroup': self.idGroup
        }