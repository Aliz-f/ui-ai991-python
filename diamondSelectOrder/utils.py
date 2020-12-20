import networkx as nx
from Base.base import Action
import matplotlib.pyplot as plt
from anytree import Node, RenderTree
from anytree.render import ContStyle
import copy
import math

# maps = list()  # List for Maps
# with open("", "r") as fin:
#     for line in fin:
#         maps.append(list(line.strip()))


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
    def __init__(self, map):
        super().__init__(map)
        self._meta_graph = nx.DiGraph()
        self._generate_meta_graph(self.goal)

    def _generate_meta_graph(self, daimond_list):
        initial_state = []
        self._meta_graph.add_node(str(initial_state))
        self._add_edge_recursively(initial_state, daimond_list)
        # Save picture of graph
        nx.draw(self._meta_graph, with_labels=True)
        plt.savefig("./res.png")  # save as png
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
                state_x, state_y, _ = state[len(state) - 1]
            except IndexError:
                agent_x, agent_y = tuple(self.agent.split(','))
                state_x, state_y = int(agent_x), int(agent_y)
            c_x_state, c_y_state, __ = item
            edge_weight = (math.fabs(state_x - c_x_state)) + \
                (math.fabs(state_y - c_y_state))
            self._meta_graph.add_edge(str(state), str(
                current_state), cost=edge_weight)
            # print(state)
            # print(current_state)
            self._add_edge_recursively(current_state, new_diamond_list)


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


# nx.draw(G, with_labels=True)
# plt.savefig("res.png")  # save as png
# plt.show()  # display
    return(G, agent, diamond, home)


def Neighbors(G, node):
    # print(list(nx.neighbors(G, node)))
    try:
        return (list(nx.neighbors(G, node)))
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


# *********************test****************************
# Create Graph
# graph, agent, diamond, home = generateGraph(maps)

# # Print Neighbors of '1,1' node
# print(Neighbors(graph, '1,1'))

# # Create Root Tree
# root = root_tree(agent)

# # Expand Tree for root
# our_list = expand_tree(graph, root)

# # Show expand tree
# tree = list()
# for item in our_list:
#     tree.append(expand_tree(graph, item))

# print(RenderTree(root, style=ContStyle))

# *************************************************
