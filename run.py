import pandas as pd
import numpy as np

import src.environment as uno


def main():
    
    winners, turns, coverage = list(), list(), list()

    params = {
        "iterations": 100,
        "algorithm": "monte-carlo",
        "logging": False,
        "model": {
            "epsilon": 0.4,
            "step_size": 0.2,
            "pre_trained": True,
        }
    }

    run = uno.tournament(
        iterations = params['iterations'],
        algo       = params['algorithm'],
        comment    = params['logging'],
        agent_info = params['model']
    )

    result = pd.concat([
        pd.Series(run[0], name='winner'), 
        pd.Series(run[1], name='turns')
    ], axis = 1)
    
    result["win_rate"] = np.where(result["winner"]=="Bernhard",1,0)
    result["win_rate"] = result["win_rate"].cumsum()/(result.index+1)

    result.to_csv("assets/results.csv")
    print('done')

if __name__ == "__main__":
    main()