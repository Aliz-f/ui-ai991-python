from utils import DiamondMiner
from Base.base import BaseAgent, Action
from sa import local_search
from search import search


class LocalSearchAgent(BaseAgent):
    sequence = []

    def do_turn(self, turn_data) -> Action:
        state = turn_data
        if not self.sequence:
            problem = DiamondMiner(state)
            problem.best_path = local_search(problem, state.turns_left)
            print('diamond order is: ', problem.best_path['order'])
            self.sequence = problem.soloution()
        if self.sequence:
            return self.sequence.pop()
