class Area:

    def __init__(self, id, areaName):
        self.id = id
        self.areaName = areaName

    def to_dict(self):
        return {
            'id': self.id,
            'areaName': self.areaName
        }
