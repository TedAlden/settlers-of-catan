class Bank:

    def __init__(self):
        self.lumber = 19
        self.wool = 19
        self.grain = 19
        self.brick = 19
        self.ore = 19

        self.card_knight = 14
        self.card_road = 2
        self.card_year_plenty = 2
        self.card_monopoly = 2
        self.card_vp = 5
    

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
