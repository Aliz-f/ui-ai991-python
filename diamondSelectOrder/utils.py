import networkx as nx
from Base.base import Action
import matplotlib.pyplot as plt
from anytree import Node, RenderTree
from anytree.render import ContStyle
import copy
import math
import re


class nodeTree (Node):
    def __init__(self, child, parent, label):
        super().__init__(child, parent=parent)

        if parent == None:
            self.gn = 0
        else:
            self.gn = parent.gn + 1

        if parent != None:
            parent_numbers = label.split(',')
            for i in range(len(parent_numbers)):
                parent_numbers[i] = int(parent_numbers[i])

            child_numbers = child.split(',')
            for i in range(len(child_numbers)):
                child_numbers[i] = int(child_numbers[i])

            for i in range(len(parent_numbers)):
                if parent_numbers[i] == child_numbers[i]:
                    if parent_numbers[i+1] == child_numbers[i+1]:
                        break
                    elif parent_numbers[i+1] > child_numbers[i+1]:
                        self.action = Action.LEFT
                        break
                    elif parent_numbers[i+1] < child_numbers[i+1]:
                        self.action = Action.RIGHT
                        break
                elif parent_numbers[i] > child_numbers[i]:
                    self.action = Action.UP
                    break
                elif parent_numbers[i] < child_numbers[i]:
                    self.action = Action.DOWN
                    break


class Graph(object):

    def __init__(self, map):
        self.problem, self.agent, self.goal, self.home = generateGraph(map)
        self.final = False

    def goal_test(self, node):
        node_tuple = tuple([int(num) for num in node.name.split(',')])
        if self.final:
            if node_tuple in self.home:
                return True
        else:
            if node_tuple in self.goal:
                return True
        return False


class MetaGraph(Graph):
    def __init__(self, state):
        super().__init__(state.map)
        self._meta_graph = nx.DiGraph()
        self.agent = state.agent_data[0].position
        self._generate_meta_graph(self.goal)
        self.diamond_order = [(0, 0, 0)]
        self.final = False

    def _generate_meta_graph(self, daimond_list):
        initial_state = []
        self._meta_graph.add_node(str(initial_state))
        self._add_edge_recursively(initial_state, daimond_list)
        # Save picture of graph
        # nx.draw(self._meta_graph, with_labels=True)
        # plt.savefig("./res.png")  # save as png
        # plt.show()  # display
        # intial_state = []
        # base_x, base_y = self.home[0]

        shortest_path_length = nx.dijkstra_path_length(
            self._meta_graph, str(initial_state), str(daimond_list), weight="cost")
        print(shortest_path_length)
        # for item in all_paths:
        # print(item)
        # for node in self._meta_graph.nodes:
        # print(node)

    def _add_edge_recursively(self, state, daimond_list):
        for i in range(len(daimond_list)):
            new_diamond_list = copy.deepcopy(daimond_list)
            item = new_diamond_list.pop(i)
            current_state = state.copy()
            current_state.append(item)
            try:
                edge_cost = self._calculate_cost(state[len(state) - 1], item)
            except IndexError:
                # edge_cost = 0
                agent_x, agent_y = self.agent
                edge_cost = self._calculate_cost((agent_x, agent_y, 0), item)

            self._meta_graph.add_edge(str(state), str(
                current_state), cost=edge_cost)
            self._add_edge_recursively(current_state, new_diamond_list)

    def _calculate_cost(self, first_state, second_state):
        cost = 0
        state_x, state_y, _ = first_state
        c_x_state, c_y_state, __ = second_state
        closest_base_length = 100
        closest_base_x, closest_base_y = None, None
        for base in self.home:
            base_x, base_y = base
            to_base_length = math.fabs(state_x - base_x) + \
                math.fabs(state_y - base_y)
            if to_base_length <= closest_base_length:
                closest_base_length = to_base_length
                closest_base_x, closest_base_y = base

        cost_to_base = math.fabs(state_x - closest_base_x) + \
            math.fabs(state_y - closest_base_y)
        cost_from_base = math.fabs(
            c_x_state - closest_base_x) + math.fabs(c_y_state - closest_base_y)
        cost = cost_to_base + cost_from_base
        return cost

    def meta_goal_test(self, state):
        if len(state.name) == len(str(self.goal)):
            return True
        return False

    def set_order(self, state):
        state = self._string_to_list(state)
        if len(self.diamond_order) == len(state):
            state.sort(key=self._sort_key)
            self.diamond_order = state
        else:
            goal_collected_score = 0
            for target in self.diamond_order:
                _1, _2, score = target
                goal_collected_score += score

            state_collected_score = 0
            for target in state:
                _1, _2, score = target
                state_collected_score += score
            if state_collected_score > goal_collected_score:
                state.sort(key=self._sort_key)
                self.diamond_order = state

        return self.diamond_order

    def _string_to_list(self, string):
        pattern = r'\d+, \d+, \d+'
        regex = re.compile(pattern)
        result = regex.findall(string)
        string_list = [res.split(',') for res in result]
        new_list = []
        for item in string_list:
            new_list.append((int(item[0]), int(item[1]), int(item[2])))

        return new_list

    def _sort_key(self, node):
        _, __, score = node
        return score

    def get_cost(self, child_state, parent_state):
        data = self._meta_graph.get_edge_data(parent_state, child_state)
        return data['cost']

    def goal_test(self, node):
        if self.final:
            for base in self.home:
                x, y = base
                goal = f'{x},{y}'
                if node.name == goal:
                    self.final = False
                    return True
        else:
            x, y, _ = self.diamond_order[len(self.diamond_order) - 1]
            diamond = f'{x},{y}'
            if node.name == diamond:
                self.diamond_order.pop()
                self.final = True
                return True
        return False


class MetaNode(Node):
    def __init__(self, graph, node, parent):
        super().__init__(node, parent=parent)
        if parent:
            self.g = graph.get_cost(node, parent.name)
        else:
            self.g = 0


def generateGraph(map):

    G = nx.Graph()  # Create Graph
    walls = list()  # List for locations Walls
    diamond = list()  # List for Location diamond
    home = list()  # Lisr fot location Homes
    maps = list()
    agent = None

    for item in map:
        maps.append(list(item))

    # Find walls, diamond, agent, homes
    for i in range(0, len(maps)):
        for j in range(0, len(maps)):
            if maps[i][j] == '*':
                walls.append(tuple((i, j)))
            elif maps[i][j].isdigit():
                diamond_score = 0
                if maps[i][j] == "0":
                    diamond_score = 2
                elif maps[i][j] == "1":
                    diamond_score = 5
                elif maps[i][j] == "2":
                    diamond_score = 3
                elif maps[i][j] == "3":
                    diamond_score = 1
                elif maps[i][j] == '4':
                    diamond_score = 10
                diamond.append((i, j, diamond_score))
            elif maps[i][j] == 'A':
                agent = f"{i},{j}"
            elif maps[i][j] == 'a':
                home.append(tuple((i, j)))

    # Add edges ==> row
    for i in range(0, len(maps)):
        for j in range(0, len(maps)):
            if tuple((i, j)) not in walls and tuple((i, j+1)) not in walls:
                if j+1 < len(maps):
                    G.add_edge(f"{i},{j}", f"{i},{j+1}")

    # Add edges ==> Column
    for j in range(0, len(maps)):
        for i in range(0, len(maps)):
            if tuple((i, j)) not in walls and tuple((i+1, j)) not in walls:
                if i+1 < len(maps):
                    G.add_edge(f"{i},{j}", f"{i+1},{j}")

    return(G, agent, diamond, home)


def Neighbors(G, node):
    try:
        return (list(nx.neighbors(G, str(node))))
    except AttributeError:
        return []


def root_tree(node):
    root = nodeTree(node, None, None)
    return root


def expand_tree(G, parent):
    list_neighbors = Neighbors(G.problem, parent.name)
    child_nodes = list()
    for neighbors in list_neighbors:
        child_nodes.append(nodeTree(neighbors, parent, parent.name))
    return child_nodes


def expand_meta_graph(graph, node):
    list_neighbors = Neighbors(graph._meta_graph, node.name)
    child_nodes = list()
    for neighbors in list_neighbors:
        child_nodes.append(MetaNode(graph, neighbors, node))
    return child_nodes
