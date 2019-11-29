import regret_matching
import numpy as np
MONICA = 0
GARY = 1
NUM_ITERATIONS = 1000000

def colonel_blotto():
    """
    Create the normal-form game

    Returns
    -------
    game : np.ndarray
    The numpy.ndarray that represents the Colonel Blotto game
    """

    actions = np.array([[3 - i -k, k, i] for i in range(4) for k in range(4 - i)])
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

def main():
    rsp = [
        [[0, 0], [-1, 1], [1, -1]],
        [[1, -1], [0, 0], [-1, 1]],
        [[-1, 1], [1, -1], [0, 0]]
    ]
    battle_of_sexes = [
        [[2, 1], [0, 0]],
        [[0, 0], [1, 2]]
    ]

    chicken = [
        [[6, 6], [2, 7]],
        [[7, 2], [0, 0]]
    ]
    cb = colonel_blotto()

    regret_matching.Player.init_game(regret_matching.Player, battle_of_sexes)

    # regret_matching
    monica_mixed_strategy = []
    monica = regret_matching.Player(MONICA)
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
    # print(f"Gary's converged strategy is {gary.cum_strategy / gary.num_played}")
    np.save("rsp_result", np.array(monica_mixed_strategy))

if __name__ == "__main__":
    main()