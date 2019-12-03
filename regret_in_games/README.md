# Regret Matching Algorithm
In this directory, I implemented the regret-matching algorithm, which seeks for a correlated equilibrium in a normal game.

You can simulate games such as rock-paper-scissors, battle of sexes, chicken game, and colonel blotto.

## How to use?
Moving to `src` directory, you run `python main.py game_name`.

Now, games to be implemented are shown in the following table.

| game_name | corresponding game |
| --------- | ------------------ |
| rsp       | rock-paper-scissors|
| bos       | battle of sexes    |
| chi       | chicken            |
| cb        | colonel blotta     |

You can define a matrix game using `numpy.array` and run the regret matching.
