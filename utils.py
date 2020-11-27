import networkx as nx
import matplotlib.pyplot as plt
from anytree import Node, RenderTree
from anytree.render import ContStyle
from base import Action

# maps = list()  # List for Maps
# with open("ui-ai991-python/Maps/map1/map.txt", "r") as fin:
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


def generateGraph(maps):
    G = nx.Graph()  # Create Graph
    walls = list()  # List for wall locations
    diamond = list()  # List for diamond Location
    home = list()  # Lisr fot Homes location
    numbers = ["0", "1", "2", "3", "4"]
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

    # Save picture of graph
    nx.draw(G, with_labels=True)
    plt.savefig("resault.png")  # save as png
    plt.show()  # display

    return(G, agent, diamond, home)


def Neighbors(G, node):
    return (list(nx.neighbors(G, node)))


def root_tree(node):
    root = nodeTree(node, None, None)
    return root


def expand_tree(G, parent):
    list_neighbors = Neighbors(G, parent.name)
    child_nodes = list()
    for neighbors in list_neighbors:
        child_nodes.append(nodeTree(neighbors, parent, parent.name))
    return child_nodes


class Graph(object):

    def __init__(self, map):
        self.problem, self.agent, self.goal, self.home = generateGraph(map)

    def goal_test(self, node):
        goal = str(self.goal[0])
        return node.name == goal


# graph, agent, diamond, home = generateGraph(maps)

# # print(Neighbors(graph,'1,1'))
# root = root_tree(graph, agent)
# our_list = expand_tree(graph, root)

# temp = list()

# for item in our_list:
#     temp.append(expand_tree(graph, item))

# print(RenderTree(root, style=ContStyle()))
