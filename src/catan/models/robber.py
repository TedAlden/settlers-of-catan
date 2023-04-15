class Robber:

    def __init__(self):
        self.owner = None
        self.hextile = None


    def get_hex(self):
        return self.hextile


    def set_hex(self, hextile):
        self.hextile = hextile


    def get_owner(self):
        return self.owner


    def set_owner(self, player):
        self.owner = player
