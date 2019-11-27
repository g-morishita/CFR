import regret_matching
MONICA = 0
GARY = 1

def main():
    battle_sexes = [
        [[2, 1], [0, 0]],
        [[0, 0], [1, 2]]
    ]
    regret_matching.Player.init_game(regret_matching.Player, battle_sexes)
    monica = regret_matching.Player(MONICA)
    gary = regret_matching.Player(GARY)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()