from os import pathsep
import networkx as nx
from anytree import Node
import matplotlib.pyplot as plt
import itertools as it
from random import randint
from Base.base import Action
from math import fabs


class DiamondMiner(object):

    def __init__(self, state):
        '''
        the class for wrapping everything needed for LocalSearch algorythm
        to find the best diamond order for gathering and then returning sequences
        of actions for the Agent to carry out
        '''
        self.problem, self.agent, self.diamonds, self.diamond_score, self.bases = generateProblem(
            state.map)
        self.agent = state.agent_data[0].position
        self.best_path = None
        self.goal_path = None
        

    def create_random_soloution(self, turns_left, initial=False, sol=None, walk=0):
        path_cost = 0
        diamond_order = []
        points_collected = 0

        # creating a permutation of this diamond order
        if initial:
            permutations = it.permutations(self.diamond_score)

            # path to achive this permutation
            perms = list(permutations)
            permutation = perms[0]
            path, points_collected, path_cost = whichDiamond(self.problem, self.agent, permutation,
                                                             self.bases, turns_left, walk)
        else:
            if not sol:
                raise "no Soloution sent"

            new_sol = self._format_to_list(sol)
            permutation = self._create_permutation(new_sol)
            path, points_collected, path_cost = whichDiamond(self.problem, self.agent, permutation,
                                                             self.bases, turns_left, walk)

        # for each_path in path:
        #     path_cost += len(each_path)

        for diamonds in permutation:
            diamond_order.append(diamonds.get('name'))

        return {
            'path': path,
            'order': diamond_order,
            'cost': path_cost,
            'score': points_collected
        }

    def goal_test(self, node):
        if not self.goal_path:
            self._generate_goal_path()
        if node.name == self.goal_path[0]:
            self.goal_path.pop(0)
            return True
        return False

    def soloution(self):
        sequence = []
        self._generate_goal_path()
        agent_x, agent_y = self.agent
        while self.goal_path:
            goal_string = self.goal_path.pop(0)
            goal = [int(x) for x in goal_string.split(',')]
            if goal[0] == agent_x and goal[1] - agent_y == 1:
                sequence.append(Action.RIGHT)
            elif goal[0] == agent_x and goal[1] - agent_y == -1:
                sequence.append(Action.LEFT)
            elif goal[0] - agent_x == 1 and goal[1] == agent_y:
                sequence.append(Action.DOWN)
            elif goal[0] - agent_x == -1 and goal[1] == agent_y:
                sequence.append(Action.UP)
            agent_x, agent_y = goal[0], goal[1]
        sequence.reverse()
        return sequence

    def _generate_goal_path(self):
        path = self.best_path['path']
        for p in path:
            if not self.goal_path:
                self.goal_path = p
                continue
            self.goal_path += p

    def _create_permutation(self, current_soloution):
        '''
        the method wich creates a permutation
        by either swapping two indices
        or reversing from one index to another
        or by inserting the first index after the second index
        with possibility
        '''
        if len(self.diamond_score) == 1:
            return current_soloution
        # creating a random number
        num = randint(0, 1)

        # swapp possibility
        p_swap = 0.6

        # reversion possibility
        p_reversion = 0.1

        # insertion possibility
        p_insertion = 0.3

        # deciding what to happen in either case of num:
        if num < p_reversion:
            return do_reverse(current_soloution)
        elif num > p_reversion and num < p_insertion:
            return do_insert(current_soloution)
        else:
            return do_swap(current_soloution)

    def _format_to_list(self, sol_dict):
        '''
        it gets a dict soloution which has path, order and cost keys
        and creates a list of dicts in order specified according to order key
        each dict in the new list has diamond name position and score
        '''
        diamond_order = sol_dict['order']
        list_sol = []
        for diamond in diamond_order:
            for element in self.diamond_score:
                if element['name'] == diamond:
                    if element not in list_sol:
                        list_sol.append(element)
                        break
        return list_sol


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


def do_swap(sol):
    '''
    swapping two indeices randomly
    '''

    # chose two indices form the array
    first_num = int(randint(0, len(sol) - 1))
    second_num = int(randint(0, len(sol) - 1))

    # making sure that first_number is not equal to second_number
    while first_num == second_num:
        second_num = int(randint(0, len(sol) - 1))

    # swap the values of the two indices
    temp = sol[first_num]
    sol[first_num] = sol[second_num]
    sol[second_num] = temp
    return sol


def do_reverse(sol):
    '''
    reversing from the first randomly generated index
     to the secomd randomly generated index
    '''

    # chose two indices form the array
    first_num = int(randint(0, len(sol) - 2))
    second_num = int(randint(first_num, len(sol) - 1))

    # making sure that the first index is lesser than the second index

    # making sure that first_number is not equal to second_number
    while first_num == second_num:
        second_num = int(randint(first_num, len(sol) - 1))
        # if first_num > second_num:
        #     temp = first_num
        #     first_num = second_num
        #     second_num = temp

    # reversing the chosen slice and recreating the sol
    reversed_particle = sol[first_num:second_num]
    reversed_particle.reverse()
    before_reversed_particle = sol[:first_num]
    after_reversed_particle = sol[second_num:]
    return before_reversed_particle + reversed_particle + after_reversed_particle


def do_insert(sol):
    '''
    inserts the first randomly chosen index
    after the second randomly chosen index
    '''

    # chose two indices form the array
    first_num = int(randint(0, len(sol) - 1))
    second_num = int(randint(0, len(sol) - 1))

    # making sure that first_number is not equal to second_number
    while first_num == second_num:
        second_num = int(randint(0, len(sol) - 1))

    # do the insertion
    element = sol.pop(second_num)
    sol.insert(first_num, element)
    return sol


def generateProblem(map):

    problem = nx.Graph()  # * Create Graph
    walls = list()  # * List for locations Walls
    diamond = list()  # * List for Location diamond
    home = list()  # * List fot location Homes
    numbers = ["0", "1", "2", "3", "4"]  # * List for found diamond
    maps = list()  # * Matrix for save map
    diamondSocre = list()  # * To save all diamonds (nested dictionary)
    agent = None  # Agent position

    # * Create nested list for map
    for item in map:
        maps.append(list(item))

    # * Find walls, diamond, diamondScores, agent, homes
    for i in range(0, len(maps)):

        for j in range(0, len(maps)):

            # * Find walls
            if maps[i][j] == '*':
                walls.append(tuple((i, j)))

            # * Find diamonds and diamondScores
            elif maps[i][j].isdigit():

                diamond.append(tuple((i, j)))

                if maps[i][j] == '0':
                    green = {'name': '0-green',
                             'position': f'{i},{j}', 'score': 2}
                    diamondSocre.append(green)

                elif maps[i][j] == '1':
                    blue = {'name': '1-blue',
                            'position': f'{i},{j}', 'score': 5}
                    diamondSocre.append(blue)

                elif maps[i][j] == '2':
                    red = {'name': '2-red', 'position': f'{i},{j}', 'score': 3}
                    diamondSocre.append(red)

                elif maps[i][j] == '3':
                    yellow = {'name': '3-yellow',
                              'position': f'{i},{j}', 'score': 1}
                    diamondSocre.append(yellow)

                elif maps[i][j] == '4':
                    gray = {'name': '4-gary',
                            'position': f'{i},{j}', 'score': 10}
                    diamondSocre.append(gray)

            # * Find agent position
            elif maps[i][j] == 'A':
                agent = f"{i},{j}"

            # * Find homes
            elif maps[i][j] == 'a':
                home.append(f'{i},{j}')

    # * Add edges ==> row
    for i in range(0, len(maps)):

        for j in range(0, len(maps)):

            if tuple((i, j)) not in walls and tuple((i, j+1)) not in walls:

                if j+1 < len(maps):
                    problem.add_edge(f"{i},{j}", f"{i},{j+1}")

    # * Add edges ==> Column
    for j in range(0, len(maps)):

        for i in range(0, len(maps)):

            if tuple((i, j)) not in walls and tuple((i+1, j)) not in walls:

                if i+1 < len(maps):
                    problem.add_edge(f"{i},{j}", f"{i+1},{j}")

    # ? Save picture of graph
    # nx.draw(problem, with_labels=True)
    # plt.savefig("./result/map5/result-map.png")  # save as png #! if run it with consol address ==> from virtualenv
    # plt.savefig("res.png")
    # plt.show()  # display

    return(problem, agent, diamond, diamondSocre, home)


def diamondOrder(problem, agent, diamondScores, homes):

    diamond_order = list()  # * To Save order of diamond for each path
    paths = dict()  # * Return all path for all permutations
    dict_iterator = 0  # * Key for create dictionary
    paths_cost = 0  # * Cost of each path
    walk = 0  # * Number of move for agent
    pointsCollected = 0  # * To calculate score for each path
    turnsLeft = 17  # ! Turns left for agent

    # * List  with all permutations for diamonds
    permutations = it.permutations(diamondScores)

    # * Cretae path for specific permutation
    for permutation in permutations:

        # * Return path for this specific permutation
        path = whichDiamond(problem, agent, permutation,
                            homes, turnsLeft, walk)

        # * Calculate cost of this path
        for each_path in path:
            paths_cost += len(each_path)

        # * Set order of diamonds for this path
        for diamonds in permutation:
            diamond_order.append(diamonds.get('name'))

        # * Calculate scores for this path
        length_path = len(path)
        i = 0
        for diamonds in permutation:
            pointsCollected += diamonds.get('score')
            i += 1
            if i == length_path:
                break

        # * cretae dictionary for all path
        paths[f'{dict_iterator}'] = {'path': path, 'order': diamond_order,
                                     'cost': paths_cost, 'score': pointsCollected}

        # Clear all temp for create other paths
        diamond_order = []
        dict_iterator += 1
        paths_cost = 0
        pointsCollected = 0

    return (paths)


def whichDiamond(graph, agent, permutation, homes, turns, walk):

    paths = list()  # * Return final path
    each_diamond = list()  # * To save path for each diamond (with home)
    pointsCollected = 0
    path_cost = 0

    if isinstance(agent, tuple):
        agent_x, agent_y = agent
        agent = f'{agent_x},{agent_y}'

    for i in range(len(permutation)):

        # * Position of diamond
        diamond_position = permutation[i].get('position')

        # * Check for initial state or not!
        if i == 0:
            diamond_path = nx.shortest_path(graph, agent, diamond_position)
        else:
            diamond_path = nx.shortest_path(
                graph, paths[-1][-1], diamond_position)

        # * Add Path for diamonds
        for j in range(1, len(diamond_path)):
            each_diamond.append(diamond_path[j])

        # * Find nearest home for diamond
        home_path = whichHome(graph, diamond_position, homes)

        # * Add path for home
        for k in range(1, len(home_path)):
            each_diamond.append(home_path[k])

        # * Check if our walk more than turns left ==> return last path
        walk += len(each_diamond)
        if walk > turns:
            step_taken = 0
            pointsCollected = 0
            path_cost = 0
            length_path = len(paths)
            i = 0
            for diamonds in permutation:
                step_taken += len(paths[i])
                if step_taken <= turns:
                    pointsCollected += diamonds.get('score')
                i += 1
                if i == length_path:
                    break
            for each_path in paths:
                path_cost += len(each_path)
            paths.append(each_diamond)

        else:
            # each list in paths shows one diamond in home
            pointsCollected = 0
            path_cost = 0
            paths.append(each_diamond)
            length_path = len(paths)
            i = 0
            for diamonds in permutation:
                pointsCollected += diamonds.get('score')
                i += 1
                if i == length_path:
                    break
            for each_path in paths:
                path_cost += len(each_path)

            each_diamond = []

    return (paths, pointsCollected, path_cost)


def whichHome(graph, diamond_pos, homes):
    homePaths = list()  # * All path to all homes in the map
    homePath = list()  # * Return final home with shortest length

    # * All shortest path for all homes
    for home in homes:
        homePaths.append(nx.all_shortest_paths(graph, diamond_pos, home))

    # * Find shortest path in homes
    min = 1000
    for each_path in homePaths:
        for path in each_path:
            length = len(path)
            if length < min:
                min = length
                homePath = path

    return homePath


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
