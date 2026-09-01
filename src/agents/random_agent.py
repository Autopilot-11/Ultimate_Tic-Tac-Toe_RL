"""A baseline agent that selects legal move randomly"""

import random

class RandomAgent:
    def __init__(self, seed:int | None = None):
        self.rng = random.Random(seed)


    def select_action(self,game) -> int:
        """Agent randomly choose from possible actions"""
        actions = game.legal_actions()

        if not actions:
            raise ValueError("Cannot select an action in a terminal game.")

        return self.rng.choice(actions)
    