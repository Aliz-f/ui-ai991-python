from utils import MetaGraph
from Base.base import BaseAgent, Action
from search import meta_graph_search, search


class MultipleDiamondAgent(BaseAgent):
    sequence0 = []
    sequence1 = []

    def do_turn(self, turn_data) -> Action:
        state = turn_data
        agent_x, agent_y = state.agent_data[0].position
        if not self.sequence0 and not self.sequence1:
            meta_problem = MetaGraph(state.map)
            meta_problem.goal_list = meta_graph_search(
                meta_problem._meta_graph, state.turns_left)
            if not state.agent_data[0].carrying:
                meta_problem.agent = f'{agent_x},{agent_y}'
                self.sequence0 = search(meta_problem.problem)
            else:
                meta_problem.agent = f'{agent_x},{agent_y}'
                meta_problem.final = True
                self.sequence1 = search(meta_problem.problem)

        if self.sequence0:
            return self.sequence0.pop()
        elif self.sequence1:
            return self.sequence1.pop()
