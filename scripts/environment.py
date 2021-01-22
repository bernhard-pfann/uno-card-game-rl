# Libraries
# -------------------------------------------------------------------------

# Custom libraries
import agents as ag
import state_action_reward as sar

# Public libraries
import numpy as np
import random
import time
from tqdm.notebook import tqdm
import sys, os


# 1. Print Functions
# -------------------------------------------------------------------------

def block_print():
    sys.__stdout__ = sys.stdout
    sys.stdout = open(os.devnull, "w")
    
def enable_print(): 
    sys.stdout = sys.__stdout__

def bold(string):
    chr_start = "\033[1m"
    chr_end = "\033[0m"
    print (chr_start + string + chr_end)
    
def underline(string):
    chr_start = "\033[4m"
    chr_end = "\033[0m"
    print(chr_start + string + chr_end)


# 2. Card
# -------------------------------------------------------------------------

class Card(object):
    """
    Card is represented as tuple with properties 'color' and 'value'. 
    Card can be evaluated if playable.
    """
    
    def __init__(self, c, v):
        self.color = c
        self.value = v
    
    
    def evaluate_card(self, open_c, open_v):
        if (self.color == open_c) or (self.value == open_v) or (self.value in ["COL","PL4"]):
            return True
    
    
    def show_card(self):
        print (self.color, self.value)
    
    
    def print_card(self):
        return str(self.color) + " " + str(self.value)


# 3. Deck
# -------------------------------------------------------------------------

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


# 4. Player
# -------------------------------------------------------------------------

class Player(object):
    """
    Player consists of a list of cards representing a players hand cards.
    Player can have a name, hand, playable hand. Thereform the players' state can be determined.
    """
    
    def __init__(self, name):
        self.name      = name
        self.hand      = list()
        self.hand_play = list()
        self.card_play = 0
        
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
    
              
    def play_agent(self, deck, card_open):
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


# 5. Turn
# -------------------------------------------------------------------------

class Turn(object):
    """
    Captures the process of a turn, that consists of:
        - Initialization of hand cards and open card before first turn
        - Chosen action by player
        - Counter action by oposite player in case of PL2 or PL4
    """
    
    def __init__(self, deck, player_1, player_2):
        """
        Turn is initialized with standard deck, players and an open card
        """
        
        self.deck = deck
        self.player_1 = player_1
        self.player_2 = player_2
        self.card_open = self.deck.draw_from_deck()
        self.start_up()
    
    
    def start_up(self):
        while self.card_open.value not in range(0,10):
            print (f'Inital open card {self.card_open.print_card()} has to be normal')
            self.card_open = self.deck.draw_from_deck()
        
        print (f'Inital open card is {self.card_open.print_card()}\n') 
        
        for i in range (7):
            self.player_1.draw(self.deck, self.card_open)
            self.player_2.draw(self.deck, self.card_open)
            
    
    def action(self, player, opponent):
        """
        Only reflecting the active players' action if he hand has not won yet.
        Only one player is leveraging the RL-algorithm, while the other makes random choices.
        """
        
        player_act = player
        player_pas = opponent
        player_act.evaluate_hand(self.card_open)

        self.count = 0
        
        # (1) When player can play a card directly
        if len(player_act.hand_play) > 0:
            
            if player_act == self.player_1:
                player_act.play_agent(self.deck, self.card_open)
            else:
                player_act.play_rand(self.deck)
                
            self.card_open = player_act.card_play
            player_act.evaluate_hand(self.card_open)

        # (2) When player has to draw a card
        else:
            print (f'{player_act.name} has no playable card')
            player_act.draw(self.deck, self.card_open)
            
            # (2a) When player draw a card that is finally playable
            if len(player_act.hand_play) > 0:
                
                if player_act == self.player_1:
                    player_act.play_agent(self.deck, self.card_open)
                else:
                    player_act.play_rand(self.deck)
                
                self.card_open = player_act.card_play
                player_act.evaluate_hand(self.card_open)
            
            # (2b) When player has not drawn a playable card, do nothing
            else:
                player_act.card_play = Card(0,0)
        
        if check_win(player_act) == True: return
        if check_win(player_pas) == True: return
        
        if player_act.card_play.value == "PL4":
            self.action_plus(player   = player_act, 
                             opponent = player_pas, 
                             penalty  = 4)
        
        if player_act.card_play.value == "PL2":
            self.action_plus(player   = player_act, 
                             opponent = player_pas, 
                             penalty  = 2)
        
        
    def action_plus(self, player, opponent, penalty):
        """
        Reflecting the process when a PL2 or PL4 is played. In case the opponent is able to counter with the same type of card he will.
        This continues until a player does not have the respective card.
        """
        
        player_act = player
        player_pas = opponent
        hit, self.count = True, 1

        while hit == True:
            hit = False
            for card in player_pas.hand:
                if card.value == "PL"+str(penalty):
                    player_pas.play_counter(self.deck, self.card_open, plus_card = card)
                    hit = True
                    self.count += 1
                    break
                    
            if check_win(player_pas) == True: return 

            if hit == True:
                hit = False
                for card in player_act.hand:
                    if card.value == "PL"+str(penalty):
                        player_act.play_counter(self.deck, self.card_open, plus_card = card) 
                        hit = True
                        self.count += 1
                        break
                        
            if check_win(player_act) == True: return
        
        
        if self.count%2 == 0:
            print (f'\n{player_act.name} has to draw {self.count*penalty} cards')
            for i in range (self.count*penalty): player_act.draw(self.deck, self.card_open)

        else:
            print (f'\n{player_pas.name} has to draw {self.count*penalty} cards')
            for i in range (self.count*penalty): player_pas.draw(self.deck, self.card_open)


# 6. Game
# -------------------------------------------------------------------------

class Game(object):
    """
    A game reflects an iteration of turns, until one player fulfills the winning condition of 0 hand cards.
    It initialized with two players and a turn object.
    """
    
    def __init__(self, player_1_name, player_2_name, starting_name, comment):
        
        if comment == False: block_print()
        
        self.player_1 = Player(player_1_name)
        self.player_2 = Player(player_2_name)
        self.turn = Turn(deck = Deck(), player_1 = self.player_1, player_2 = self.player_2)
        
        self.turn_no = 0
        self.winner = 0

        # With each new game the starting player is switched, in order to make it fair
        while self.winner == 0:
            self.turn_no += 1
            card_open = self.turn.card_open
            bold (f'\n---------- TURN {self.turn_no} ----------')
            print (f'\nCurrent open card: {self.turn.card_open.print_card()}')

            if starting_name == self.player_1.name:
                if self.turn_no%2 == 1: player_act, player_pas = self.player_1, self.player_2
                else:                   player_act, player_pas = self.player_2, self.player_1
            else:
                if self.turn_no%2 == 0: player_act, player_pas = self.player_1, self.player_2
                else:                   player_act, player_pas = self.player_2, self.player_1

            player_act.show_hand()
            player_act.show_hand_play(card_open)
            self.turn.action(player = player_act, opponent = player_pas)
            
            if check_win(player_act) == True:
                self.winner = player_act.name
                print (f'{player_act.name} has won!')
                break
                
            if check_win(player_pas) == True:
                self.winner = player_pas.name
                print (f'{player_pas.name} has won!')
                break
                
            if player_act.card_play.value in ["REV", "SKIP"]:
                print (f'{player_act.name} has another turn')
                self.turn_no = self.turn_no-1
                
            if (self.turn.count > 0) and (self.turn.count %2 == 0):
                print (f'Again it is {player_act.name}s turn')
                self.turn_no = self.turn_no-1
        

        self.player_1.identify_state(card_open)
        agent.update(self.player_1.state, self.player_1.action)
                
        if comment == False: enable_print()


# 7. Tournament
# -------------------------------------------------------------------------

def tournament(iterations, algo, comment, agent_info):
    """
    A function that iterates various Games and outputs summary statistics over all executed simulations.
    """

    timer_start = time.time()
    
    # Selection of algorithm
    global agent, algorithm
    algorithm = algo
    
    if algo == "q-learning":
        agent = ag.QLearningAgent()
    else:
        agent = ag.MonteCarloAgent()
    
    
    winners, turns, coverage = list(), list(), list()
    agent.agent_init(agent_info)

    for i in tqdm(range(iterations)):
        time.sleep(0.01)

        if i%2 == 1:
            game = Game(player_1_name = "Bernhard", 
                        player_2_name = "Magdalena",
                        starting_name = "Magdalena",
                        comment = comment)
        else:
            game = Game(player_1_name = "Bernhard", 
                        player_2_name = "Magdalena",
                        starting_name = "Bernhard",
                        comment = comment)

        winners.append(game.winner)
        turns.append(game.turn_no)
        coverage.append((agent.q != 0).values.sum())

    # Timer
    timer_end = time.time()
    timer_dur = timer_end - timer_start
    print (f'Execution lasted {round(timer_dur/60,2)} minutes ({round(iterations/timer_dur,2)} games per second)')
    
    return winners, turns, coverage


# 8. Winning Condition
# -------------------------------------------------------------------------

def check_win(player):
    if len(player.hand) == 0:
        return True