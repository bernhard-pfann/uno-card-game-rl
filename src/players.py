import random
from src.utils import underline


class Player(object):
    """
    Player consists of a list of cards representing a players hand cards.
    Player can have a name, hand, playable hand. Thereform the players' state can be determined.
    """
    
    def __init__(self, name, agent):
        self.name         = name
        self.hand         = list()
        self.hand_play    = list()
        self.card_play    = 0
        self.state        = dict()
        self.actions      = dict()
        self.action       = 0
        agent.prev_state  = 0
    
    def evaluate_hand(self, card_open):
        """
        Loops through each card in players' hand. Evaluation depends on card open.
        Required parameters: card_open as card
        """
        
        self.hand_play.clear()
        for card in self.hand:
            if card.evaluate_card(card_open.color, card_open.value) == True:
                self.hand_play.append(card)
    
    def draw(self, deck, card_open):
        """
        Adds a card to players' hand and evaluates the hand
        Required parameters:
            - deck as deck
            - card_open as card
        """
        
        card = deck.draw_from_deck()
        self.hand.append(card)
        self.evaluate_hand(card_open)
        print (f'{self.name} draws {card.print_card()}')
        
    def identify_state(self, card_open):
        """
        The state of the player is identified by looping through players' hand for each property of the state.
        """
        norm_cards = {"RED":2,"GRE":2,"BLU":2,"YEL":2}
        spec_cards = {"SKI":1,"REV":1,"PL2":1}
        wild_cards = {"PL4":1,"COL":1}
    
        self.state = dict()
        self.state["OPEN"] = card_open.color
        if self.state["OPEN"] not in ["RED","GRE","BLU","YEL"]: random.choice(["RED","GRE","BLU","YEL"])
        
        # (1) State properties: normal hand cards
        for key, val in zip(norm_cards.keys(), norm_cards.values()):
                self.state[key] = min([1 if (card.color == key) and (card.value in range(0,10)) else 0 for card in self.hand].count(1),val)
        
        # (2) State properties: special hand cards
        for key, val in zip(spec_cards.keys(), spec_cards.values()):
                self.state[key] = min([1 if (card.value == key) else 0 for card in self.hand].count(1),val)
        
        # (3) State properties: wild hand cards
        for key, val in zip(wild_cards.keys(), wild_cards.values()):
                self.state[key] = min([1 if (card.value == key) else 0 for card in self.hand].count(1),val)
        
        # (4) State properties: normal playable cards
        for key, val in zip(norm_cards.keys(), norm_cards.values()):
                self.state[key+"#"] = min([1 if (card.color == key) and (card.value in range(0,10)) else 0 for card in self.hand_play].count(1),val-1)
        
        # (5) State properties: special playable cards
        for key, val in zip(spec_cards.keys(), spec_cards.values()):
                self.state[key+"#"] = min([1 if card.value == key else 0 for card in self.hand_play].count(1),val)
    
    def identify_action(self):
        """
        All actions are evaluated if they are available to the player, dependent on his hand and card_open.
        """
        norm_cards = {"RED":2,"GRE":2,"BLU":2,"YEL":2}
        spec_cards = {"SKI":1,"REV":1,"PL2":1}
        wild_cards = {"PL4":1,"COL":1}
        
        # (1) Action properties: normal playable cards
        for key in norm_cards.keys():
            self.actions[key] = min([1 if (card.color == key) and (card.value in range(0,10)) else 0 for card in self.hand_play].count(1),1)
        
        # (2) Action properties: special playable cards
        for key in spec_cards.keys():
            self.actions[key] = min([1 if card.value == key else 0 for card in self.hand_play].count(1),1)
        
        # (3) Action properties: wild playable cards
        for key in wild_cards.keys():
            self.actions[key] = min([1 if card.value == key else 0 for card in self.hand_play].count(1),1)
     
    def play_agent(self, deck, card_open, agent, algorithm):
        """
        Reflecting a players' intelligent move supported by the RL-algorithm, that consists of:
            - Identification of the players' state and available actions
            - Choose card_played
            - Remove card from hand & replace card_open with it
            - Update Q-values in case of TD
            
        Required parameters:
            - deck as deck
            - card_open as card
        """
        # Identify state & actions for action selection
        self.identify_state(card_open)
        self.identify_action()
        
        # Agent selects action
        self.action = agent.step(self.state, self.actions)

        # Selected action searches corresponding card
        # (1) Playing wild card
        if self.action in ["COL","PL4"]:
            for card in self.hand:            
                if card.value == self.action:
                    break

        # (2) Playing normal card with different color
        elif (self.action in ["RED","GRE","BLU", "YEL"]) and (self.action != card_open.color):
            for card in self.hand:
                if (card.color == self.action) and (card.value == card_open.value):
                    break

        # (3) Playing normal card with same color
        elif (self.action in ["RED","GRE","BLU", "YEL"]) and (self.action == card_open.color):
            for card in self.hand:
                if (card.color == self.action) and (card.value in range(0,10)):
                    break

        # (4) Playing special card with same color
        elif (self.action not in ["RED","GRE","BLU", "YEL"]) and (self.action != card_open.value):
            for card in self.hand:
                if (card.color == card_open.color) and (card.value == self.action):
                    break

        # (5) Playing special card with different color
        else:
            for card in self.hand:
                if card.value == self.action:
                    break

        # Selected card is played
        self.card_play = card
        self.hand.remove(card)
        self.hand_play.pop()
        deck.discard(card)
        print (f'\n{self.name} plays {card.print_card()}')

        if (self.card_play.value in ["COL","PL4"]):
            self.card_play.color = self.choose_color()
        
        # Update Q Value           
        if algorithm == "q-learning":
            agent.update(self.state, self.action)      

    def play_rand(self, deck):
        """
        Reflecting a players' random move, that consists of:
            - Shuffling players' hand cards
            - Lopping through hand cards and choosing the first available hand card to be played
            - Remove card from hand & replace card_open with it
        
        Required parameters: deck as deck
        """
        
        random.shuffle(self.hand_play)
        for card in self.hand:
            if card == self.hand_play[-1]:
                self.card_play = card
                self.hand.remove(card)
                self.hand_play.pop()
                deck.discard(card)
                print (f'\n{self.name} plays {card.print_card()}')
                break

        if (self.card_play.color == "WILD") or (self.card_play.value == "PL4"):
            self.card_play.color = self.choose_color()  
            
    def play_counter(self, deck, card_open, plus_card):
        """
        Reflecting a players' counter move to a plus card.
        Required parameters:
            - deck as deck
            - card_open as card
            - plus_card as card
        """
        
        for card in self.hand:
            if card == plus_card:
                self.card_play = card
                self.hand.remove(card)
                deck.discard(card)
                self.evaluate_hand(card_open)
                print (f'{self.name} counters with {card.print_card()}')
                break
        
    def choose_color(self):
        """
        Chooses a card color when a player plays PL4 or WILD COL.
        Color is determined by the majority color in the active players' hand.
        """
        
        colors = [card.color for card in self.hand if card.color in ["RED","GRE","BLU","YEL"]]
        if len(colors)>0:
            max_color = max(colors, key = colors.count)
        else:
            max_color = random.choice(["RED","GRE","BLU","YEL"])

        print (f'{self.name} chooses {max_color}')
        return max_color
    
    def show_hand(self):
        underline (f'\n{self.name}s hand:')
        for card in self.hand:
            card.show_card()
        
    def show_hand_play(self, card_open):
        underline (f'\n{self.name}s playable hand:')
        self.evaluate_hand(card_open)
        for card in self.hand_play:
            card.show_card()