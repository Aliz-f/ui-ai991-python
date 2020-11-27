from utils import *
from base import BaseAgent , TurnData , AgentData

def search(problem):
    pass


class DumpAgent(BaseAgent):
    
    def do_turn(self, turn_data : TurnData):
        sequence = list()
        state = None 
        state = self.updateState(state , turn_data)
        if not sequence:
            #goal
            #problem
            problem, ag, goal, home = generateGraph(maps)
            #sequence<==search
            sequence = search(problem)
            if not sequence:
                return None
            return sequence.pop()

    def updateState(self, state , percept: TurnData):
        if percept.turns_left == 0:
            pass
        else:
            state.position = percept.agent_data.position
            state.carrying = percept.agent_data.carrying
            state.collected = percept.agent_data.collected
        return state        
        
    