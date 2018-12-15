class Chat:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def to_dict(self):
        return {
            'name': self.name,
            'text': self.text
        }