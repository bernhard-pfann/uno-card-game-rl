import time

from src.agents import QLearningAgent, MonteCarloAgent
from src.players import Player
from src.turn import Turn
from src.cards import Card, Deck
from src.utils import check_win, block_print, enable_print, bold
import config as conf


class Game(object):
    """
    A game reflects an iteration of turns, until one player fulfills the winning condition of 0 hand cards.
    It initialized with two players and a turn object.
    """
    def __init__(self, player_1_name, player_2_name, starting_name, agent, algorithm, comment):
        
        if comment == False: block_print()
        
        self.player_1 = Player(player_1_name, agent=agent)
        self.player_2 = Player(player_2_name, agent=agent)
        self.turn = Turn(
            deck=Deck(), 
            player_1=self.player_1, 
            player_2=self.player_2, 
            agent=agent
        )
        
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
            self.turn.action(
                player=player_act, 
                opponent=player_pas, 
                agent=agent,
                algorithm=algorithm
            )
            
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


def tournament(iterations, algo, comment, agent_info):
    """
    A function that iterates various Games and outputs summary statistics over all executed simulations.
    """
    timer_start = time.time()
    
    # Selection of algorithm
    global agent, algorithm
    algorithm = algo
    
    if algo == "q-learning":
        agent = QLearningAgent(agent_info)
    else:
        agent = MonteCarloAgent(agent_info)
    
    winners, turns, coverage = list(), list(), list()

    for i in range(iterations):
        time.sleep(0.01)

        if i%2 == 1:
            game = Game(
                player_1_name=conf.player_name_1, 
                player_2_name=conf.player_name_2,
                starting_name=conf.player_name_2,
                agent=agent,
                algorithm=algo,
                comment=comment
            )
        else:
            game = Game(
                player_1_name=conf.player_name_1, 
                player_2_name=conf.player_name_2,
                starting_name=conf.player_name_1,
                agent=agent,
                algorithm=algo,
                comment=comment
            )

        winners.append(game.winner)
        turns.append(game.turn_no)
        coverage.append((agent.q != 0).values.sum())

    # Timer
    timer_end = time.time()
    timer_dur = timer_end - timer_start
    print (f'Execution lasted {round(timer_dur/60,2)} minutes ({round(iterations/timer_dur,2)} games per second)')
    
    return winners, turns, agent