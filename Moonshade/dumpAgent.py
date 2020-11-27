from utils import Graph
from search import search
from Base.base import BaseAgent, Action


class DumpAgent(BaseAgent):

    sequence = list()

    def do_turn(self, turn_data) -> Action:
        state = turn_data
        # state = self.updateState(state, turn_data)
        if not self.sequence:
            problem = Graph(state.map)
            self.sequence = search(problem)
            if not self.sequence:
                return None
            return self.sequence.pop()

    def updateState(self, state, percept):
        if percept.turns_left == 0:
            pass
        else:
            state.position = percept.agent_data.position
            state.carrying = percept.agent_data.carrying
            state.collected = percept.agent_data.collected
        return state
