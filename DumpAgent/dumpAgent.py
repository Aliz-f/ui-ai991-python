from utils import Graph
from search import search
from Base.base import BaseAgent, Action
from time import time


class DumpAgent(BaseAgent):

    sequence0 = list()
    sequence1 = list()

    def do_turn(self, turn_data) -> Action:
        state = turn_data
        # state = self.updateState(state, turn_data)
        if not self.sequence0 and not self.sequence1:
            start_time = time()
            problem = Graph(state.map)
            if not state.agent_data[0].carrying:
                agentx, agenty = turn_data.agent_data[0].position
                problem.agent = f'{agentx},{agenty}'
                self.sequence0 = search(problem)
                end_time = time()
                total = end_time - start_time
                print(
                    f'the total searching time to find the diamond is {total}')
            else:
                problem.final = True
                agentx, agenty = turn_data.agent_data[0].position
                problem.agent = f'{agentx},{agenty}'
                self.sequence1 = search(problem)
                end_time = time()
                total = end_time - start_time
                print(f'the total searching time to find the home is {total}')
            # if not self.sequence:
            # return None
        if self.sequence0:
            return self.sequence0.pop()
        elif self.sequence1:
            return self.sequence1.pop()

    def updateState(self, state, percept):
        if percept.turns_left == 0:
            pass
        else:
            state.position = percept.agent_data.position
            state.carrying = percept.agent_data.carrying
            state.collected = percept.agent_data.collected
        return state
