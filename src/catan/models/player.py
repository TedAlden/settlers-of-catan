class Player:

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

        self.vp = 0
        
        self.lumber = 0
        self.wool = 0
        self.grain = 0
        self.brick = 0
        self.ore = 0

        self.card_knight = 0
        self.card_road = 0
        self.card_year_plenty = 0
        self.card_monopoly = 0
        self.card_vp = 0
        
        self.cities = 0
        self.settlements = 0
        self.roads = 0

        # FIXME: when placing roads/settlements make sure limit is not
        # exceded, i.e. 15 roads max


    def count_settlements(self):
        return self.settlements
    

    def count_roads(self):
        return self.roads
    

    def count_cities(self):
        return self.cities
    

    def count_vp(self):
        return self.vp
    

    def count_longest_road(self):
        return 0
    

    def count_army(self):
        return self.card_knight
    

    def count_lumber(self):
        return self.lumber
    

    def count_wool(self):
        return self.wool
    

    def count_grain(self):
        return self.grain
    

    def count_brick(self):
        return self.brick
    

    def count_ore(self):
        return self.ore
    

    def count_resource_cards(self):
        return sum((
            self.lumber,
            self.wool,
            self.grain,
            self.brick,
            self.ore
        ))


    def count_development_cards(self):
        return sum((
            self.card_knight,
            self.card_road,
            self.card_year_plenty,
            self.card_monopoly,
            self.card_vp
        ))
    

    def has_resources(self, lumber=0, wool=0, grain=0, brick=0, ore=0):
        # e.g. for a road, use player1.has_resources(lumber=1, brick=1)
        return all((
            self.lumber >= lumber,
            self.wool >= wool,
            self.grain >= grain,
            self.brick >= brick,
            self.ore >= ore
        ))


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
