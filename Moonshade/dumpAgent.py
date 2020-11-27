from utils import Graph
from search import search
from Base.base import BaseAgent, Action


class DumpAgent(BaseAgent):

    sequence0 = list()
    sequence1 = list()

    def do_turn(self, turn_data) -> Action:
        state = turn_data
        # state = self.updateState(state, turn_data)
        if not self.sequence0 or self.sequence1:
            problem = Graph(state.map)
            if not state.agent_data[0].carrying:
                agentx, agenty = turn_data.agent_data[0].position
                problem.agent = f'{agentx},{agenty}'
                self.sequence0 = search(problem)
            else:
                problem.final = True
                problem.agent = agentx, agenty = turn_data.agent_data[0].position
                problem.agent = f'{agentx},{agenty}'
                self.sequence1 = search(problem)
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
