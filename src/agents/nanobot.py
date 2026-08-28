class NanoBot:
    def __init__(self, id):
        self.id = id
        self.health = 100

    def act(self):
        return 'repair'
