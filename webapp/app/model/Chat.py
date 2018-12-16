class Chat:
    def __init__(self, textC, areaName, idGroup, idUser):
        self.textC = textC
        self.areaName = areaName
        self.idUser = idUser
        self.idGroup = idGroup

    def to_dict(self):
        return {
            'textC': self.textC,
            'area': self.areaName,
            'idUser': self.idUser,
            'idGroup': self.idGroup
        }