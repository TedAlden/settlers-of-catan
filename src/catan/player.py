class Player:

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        
        self.num_settlements = 0
        self.num_roads = 0
        # FIXME: when placing roads/settlements make sure limit is not
        # exceded, i.e. 15 roads max

        # TODO: turn player.num_roads into player.roads which is a list
        # of pointers to the roads owned. Then can use len() instead