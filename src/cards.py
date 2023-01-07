import random


class Card(object):
    """
    Card is represented as tuple with properties 'color' and 'value'. 
    Card can be evaluated if playable.
    """
    def __init__(self, c, v):
        self.color = c
        self.value = v
    
    def evaluate_card(self, open_c, open_v):
        if (
            (self.color == open_c) or 
            (self.value == open_v) or 
            (self.value in ["COL","PL4"])
        ):
            return True
    
    def show_card(self):
        print (self.color, self.value)
    
    def print_card(self):
        return str(self.color) + " " + str(self.value)


class Deck(object):
    """
    Deck consists of list of cards. Is initialized with standard list of cards.
    Deck can be shuffled, drawn from.
    """
    def __init__(self):
        self.cards = []
        self.cards_disc = []
        self.build()
        self.shuffle()
    
    
    def build(self):
        colors = ["RED","GRE","BLU","YEL"]

        cards_zero   = [Card(c,0) for c in colors]
        cards_normal = [Card(c,v) for c in colors for v in range (1,10)]*2
        cards_action = [Card(c,v) for c in colors for v in ["SKI","REV","PL2"]]*2
        cards_wild   = [Card("WILD",v) for v in ["COL","PL4"]]*4
        
        cards_all = cards_normal + cards_action + cards_zero + cards_wild
        for card in cards_all: self.cards.append(card)
    
    def discard(self, card):
        self.cards_disc.append(card)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw_from_deck(self):
        if len(self.cards) == 0:
            self.cards = self.cards_disc
            self.cards_disc = []
            
        return self.cards.pop()
    
    def show_deck(self):
        for c in self.cards:
            c.show_card()
    
    def show_discarded(self):
        for c in self.cards_disc:
            c.show_card()