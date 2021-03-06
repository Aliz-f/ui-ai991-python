import networkx as nx
from Base.base import Action
import matplotlib.pyplot as plt
from anytree import Node, RenderTree
from anytree.render import ContStyle

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


def generateGraph(map):

    G = nx.Graph()  # Create Graph
    walls = list()  # List for locations Walls
    diamond = list()  # List for Location diamond
    home = list()  # Lisr fot location Homes
    numbers = ["0", "1", "2", "3", "4"]  # List for found diamond
    maps = list()
    agent = None

    for item in map:
        maps.append(list(item))

    # Find walls, diamond, agent, homes
    for i in range(0, len(maps)):
        for j in range(0, len(maps)):
            if maps[i][j] == '*':
                walls.append(tuple((i, j)))
            elif maps[i][j] in numbers:
                diamond.append(tuple((i, j)))
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
