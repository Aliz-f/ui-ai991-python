import itertools
from utils import *
from soloution import soloution


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
