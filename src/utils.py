import numpy as np
import random
import time
import sys 
import os

import src.agents as ag
import src.state_action_reward as sar
import config as conf


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

def check_win(player):
    if len(player.hand) == 0:
        return True