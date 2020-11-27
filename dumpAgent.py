from utils import Graph
from search import search
from base import BaseAgent


class DumpAgent(BaseAgent):

    def do_turn(self, turn_data):
        sequence = []
        state = turn_data
        # state = self.updateState(state, turn_data)
        if not sequence:
            problem = Graph(state.map)
            sequence = search(problem)
            if not sequence:
                return None
            return sequence.pop()

    def updateState(self, state, percept: TurnData):
        if percept.turns_left == 0:
            pass
        else:
            state.position = percept.agent_data.position
            state.carrying = percept.agent_data.carrying
            state.collected = percept.agent_data.collected
        return state
