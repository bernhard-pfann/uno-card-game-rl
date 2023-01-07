from src.cards import Card
from src.utils import check_win


class Turn(object):
    """
    Captures the process of a turn, that consists of:
        - Initialization of hand cards and open card before first turn
        - Chosen action by player
        - Counter action by oposite player in case of PL2 or PL4
    """
    def __init__(self, deck, player_1, player_2, agent):
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
            
    def action(self, player, opponent, agent, algorithm):
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
                player_act.play_agent(self.deck, self.card_open, agent, algorithm)
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
                    player_act.play_agent(self.deck, self.card_open, agent, algorithm)
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