import regret_matching
import numpy as np
import sys
MONICA = 0
GARY = 1
NUM_ITERATIONS = 100000

def colonel_blotto():
    """
    Create the normal-form game

    Returns
    -------
    game : np.ndarray
    The numpy.ndarray that represents the Colonel Blotto game

    Note
    -------
    The map of strategies is below.
    {0: array([5, 0, 0]),
     1: array([4, 1, 0]),
     2: array([3, 2, 0]),
     3: array([2, 3, 0]),
     4: array([1, 4, 0]),
     5: array([0, 5, 0]),
     6: array([4, 0, 1]),
     7: array([3, 1, 1]),
     8: array([2, 2, 1]),
     9: array([1, 3, 1]),
     10: array([0, 4, 1]),
     11: array([3, 0, 2]),
     12: array([2, 1, 2]),
     13: array([1, 2, 2]),
     14: array([0, 3, 2]),
     15: array([2, 0, 3]),
     16: array([1, 1, 3]),
     17: array([0, 2, 3]),
     18: array([1, 0, 4]),
     19: array([0, 1, 4]),
     20: array([0, 0, 5])}
    """

    NUM_SOLDIERS = 5
    actions = np.array([[NUM_SOLDIERS - i -k, k, i] for i in range(NUM_SOLDIERS + 1) for k in range(NUM_SOLDIERS + 1 - i)])
    num_actions = len(actions)
    map_actions = dict(zip(range(num_actions), actions))
    game = [[[] for _ in range(num_actions)] for _ in range(num_actions)]
    for row_action in range(num_actions):
        for col_action in range(num_actions):
            num_row_wins = (map_actions[row_action] > map_actions[col_action])[map_actions[row_action] != map_actions[col_action]]
            if num_row_wins.sum() > (~num_row_wins).sum():
                game[row_action][col_action] = [1, -1]
            elif num_row_wins.sum() < (~num_row_wins).sum():
                game[row_action][col_action] = [-1, 1]
            else:
                game[row_action][col_action] = [0, 0]
    return np.array(game)

def main(game_name):
    if game_name == "rsp":
        game = [
            [[0, 0], [-1, 1], [1, -1]],
            [[1, -1], [0, 0], [-1, 1]],
            [[-1, 1], [1, -1], [0, 0]]
        ]
    elif game_name == "bos":
        game = [
            [[2, 1], [0, 0]],
            [[0, 0], [1, 2]]
        ]
    elif game_name == "chi":
        game = [
            [[6, 6], [2, 7]],
            [[7, 2], [0, 0]]
        ]
    elif game_name == "cb":
        game = colonel_blotto()
    else:
        print(f"There is no game such as {game_name}")

    regret_matching.Player.init_game(regret_matching.Player, game)

    # regret_matching
    monica_mixed_strategy = []
    monica = regret_matching.Player(MONICA)
    # gary_initial_strategy = np.zeros(21)
    # gary_initial_strategy[13] = 1
    gary = regret_matching.Player(GARY)
    for _ in range(NUM_ITERATIONS):
        _, played_pure_strategies = monica.simulate_game([gary])
        monica.update_cum_regret(played_pure_strategies)
        monica.update_strategy()
        monica_mixed_strategy.append(monica.cum_strategy / monica.num_played)

        _, played_pure_strategies = gary.simulate_game([monica])
        gary.update_cum_regret(played_pure_strategies)
        gary.update_strategy()

    print(f"Monica's converged strategy is {monica.cum_strategy / monica.num_played}")
    print(f"Monica's final strategy is {monica.strategy}")
    print(f"Gary's converged strategy is {gary.cum_strategy / gary.num_played}")
    print(f"Gary's final strategy is {gary.strategy}")
    np.save("rsp_result", np.array(monica_mixed_strategy))

if __name__ == "__main__":
    game_name = sys.argv[1]
    main(game_name)