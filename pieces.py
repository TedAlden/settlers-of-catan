class Node:

    def __init__(self, value):
        self.value = value
        self.screen_coord = (0, 0)

    def __repr__(self):
        return self.__class__.__name__ + str(self.value)


class Terrain(Node):
 
    def __init__(self, axial_coord):
        super().__init__(None)
        self.axial_coord = axial_coord

    def __repr__(self):
        return f"{self.__class__.__name__}({self.axial_coord[0]},{self.axial_coord[1]})"


class Settlement(Node):

    def __init__(self, value):
        super().__init__(value)