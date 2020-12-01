from utils import heuristic_list, Graph
from Base.base import BaseAgent, TurnData, Action
from search import graph_search
from time import time


class SmartAgent(BaseAgent):
    sequence0 = list()
    sequence1 = list()

    def do_turn(self, turn_data: TurnData) -> Action:
        state = turn_data
        agent_x, agent_y = state.agent_data[0].position
        if not self.sequence0 and not self.sequence1:
            start_time = time()
            problem = Graph(state.map)
            if not state.agent_data[0].carrying:
                problem.agent = f'{agent_x},{agent_y}'
                heuristics = heuristic_list(problem)
                self.sequence0 = graph_search(problem, heuristics)
                end_time = time()
                total = end_time - start_time
                print(
                    f'the total searching time to find the diamond is {total}')
            else:
                problem.agent = f'{agent_x},{agent_y}'
                problem.final = True
                heuristics = heuristic_list(problem)
                self.sequence1 = graph_search(problem, heuristics)
                end_time = time()
                total = end_time - start_time
                print(f'the total searching time to find the home is {total}')
        if self.sequence0:
            return self.sequence0.pop()
        elif self.sequence1:
            return self.sequence1.pop()
