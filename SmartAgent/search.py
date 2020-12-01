from utils import nodeTree, PriorityQueue, expand_tree
from soloution import soloution


def graph_search(problem, heuristics):
    count = 0
    node = nodeTree(problem.agent, None, None, heuristics[problem.agent])
    frontier = PriorityQueue()
    frontier.insert(node)
    explored = []
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node):
            print(f'the total nodes expanded: {count}')
            return soloution(node)
        explored.append(node)
        count += 1
        children = expand_tree(problem, node, heuristics)
        for child in children:
            if not frontier.has_item(child) and child not in explored:
                frontier.insert(child)
    return
