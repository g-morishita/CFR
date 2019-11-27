import regret_matching
import numpy as np
MONICA = 0
GARY = 1
NUM_ITERATIONS = 10000

def main():
    rsp = [
        [[0, 0], [-1, 1], [1, -1]],
        [[1, -1], [0, 0], [-1, 1]],
        [[-1, 1], [1, -1], [0, 0]]
    ]
    battle_of_sexes = [
        [[100, 2], [0, 0]],
        [[0, 0], [2, 100]]
    ]

    chicken = [
        [[6, 6], [2, 7]],
        [[7, 2], [0, 0]]
    ]

    regret_matching.Player.init_game(regret_matching.Player, rsp)
    monica = regret_matching.Player(MONICA)
    gary = regret_matching.Player(GARY)

    # regret_matching
    monica_mixed_strategy = []
    for _ in range(NUM_ITERATIONS):
        _, played_pure_strategies = monica.simulate_game([gary])
        monica.update_cum_regret(played_pure_strategies)
        monica_mixed_strategy.append(monica.regret_sum / monica.regret_sum.sum())
        _, played_pure_strategies = gary.simulate_game([monica])
        gary.update_cum_regret(played_pure_strategies)
    print(f"Monica's converged strategy is {monica.regret_sum / monica.regret_sum.sum()}")
    print(f"Gary's converged strategy is {gary.regret_sum / gary.regret_sum.sum()}")
    np.save("rsp_result", np.array(monica_mixed_strategy))



if __name__ == "__main__":
    main()