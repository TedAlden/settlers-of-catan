class Node:

    def __init__(self, value):
        self.value = value
        self.coord = (0, 0)

    def __repr__(self):
        return self.__class__.__name__ + str(self.value)


class Terrain(Node):
 
    def __init__(self, tilecoord):
        super().__init__(None)
        self.tile_coord = tilecoord

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tile_coord[0]},{self.tile_coord[1]})"


class Settlement(Node):

    def __init__(self, value):
        super().__init__(value)