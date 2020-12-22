from utils import MetaNode, expand_meta_graph, expand_tree, root_tree
from queue import Queue
from soloution import soloution

import itertools


def meta_graph_search(problem, max_turns):
    node = MetaNode(problem, '[]', None)
    frontier = Queue()
    frontier.put(node)
    while frontier:
        node = frontier.get()
        max_turns -= node.g
        if problem.meta_goal_test(node):
            if max_turns > 0:
                problem.set_order(node.name)
            return problem.set_order(node.name)
        children = expand_meta_graph(problem, node)
        for child in children:
            if max_turns > 0:
                frontier.put(child)
            elif not frontier.empty():
                problem.set_order(child.name)
            else:
                return problem.set_order(child.name)


def recursive_dls(node, problem, limit):
    if problem.goal_test(node):
        return soloution(node)
    elif limit == 0:
        return
    else:
        children = expand_tree(problem, node)
        for child in children:
            result = recursive_dls(child, problem, limit - 1)
            if result:
                return result
        return None


def depth_limited_search(node, problem, limit):
    root_node = root_tree(node)
    return recursive_dls(root_node, problem, limit)


def search(problem):
    for depth in itertools.count(start=0):
        result = depth_limited_search(problem.agent, problem, depth)
        if result:
            return result
