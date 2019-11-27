# What's This?
This repository is implementations of algorithms to calculate Nash equilibria (NE).
I implement them in Python.
It is not efficient, but easy to read.

# Algorithm to implement
## Regret Matching 
This is a fundamental algorithm to seek for a correlated equilibrium which is a weaker concept of NE in a normal-form game.

### How to use
Move to `regret_in_games/src`, then just run `python main.py`. 
The requirement is python3.7 and some basic packages such as numpy, and pandas.

# Reference 
- [Neller, Todd W. and Marc Lanctot. “An Introduction to Counterfactual Regret Minimization.” (2013).](https://pdfs.semanticscholar.org/0184/855c7baafdbcadcab967d4bfa7d4f8b86285.pdf)
- Hart, Sergiu and Andreu Mas-Colell. “A Simple Adaptive Procedure Leading to Correlated Equilibrium.” (1997).
