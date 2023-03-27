class Player:

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        
        self.lumber = 0
        self.wool = 0
        self.grain = 0
        self.brick = 0
        self.ore = 0
        
        self.num_cities = 0
        self.num_settlements = 0
        self.num_roads = 0
        # FIXME: when placing roads/settlements make sure limit is not
        # exceded, i.e. 15 roads max 

        # TODO: turn player.num_roads into player.roads which is a list
        # of pointers to the roads owned. Then can use len() instead


    def count_settlements(self):
        return self.num_settlements
    

    def count_roads(self):
        return self.num_roads
    

    def count_cities(self):
        return self.num_cities
    

    def has_resources(self, lumber=0, wool=0, grain=0, brick=0, ore=0):
        # e.g. for a road, use player1.has_resources(lumber=1, brick=1)
        return self.lumber >= lumber \
            and self.wool >= wool \
            and self.grain >= grain \
            and self.brick >= brick \
            and self.ore >= ore


    def add_resources(self, lumber=0, wool=0, grain=0, brick=0, ore=0):
        self.lumber += lumber
        self.wool += wool
        self.grain += grain
        self.brick += brick
        self.ore += ore


    def remove_resources(self, lumber=0, wool=0, grain=0, brick=0, ore=0):
        self.lumber -= lumber
        self.wool -= wool
        self.grain -= grain
        self.brick -= brick
        self.ore -= ore
