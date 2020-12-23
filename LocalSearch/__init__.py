from os import pathsep
import networkx as nx
import matplotlib.pyplot as plt
import itertools as it

def generateProblem(map):

    problem = nx.Graph()                    #* Create Graph
    walls = list()                          #* List for locations Walls
    diamond = list()                        #* List for Location diamond
    home = list()                           #* List fot location Homes
    numbers = ["0", "1", "2", "3", "4"]     #* List for found diamond
    maps = list()                           #* Matrix for save map
    diamondSocre = list()                   #* To save all diamonds (nested dictionary)
    agent = None                            #  Agent position 

    #* Create nested list for map
    for item in map:
        maps.append(list(item))

    #* Find walls, diamond, diamondScores, agent, homes
    for i in range(0, len(maps)):
        
        for j in range(0, len(maps)):
            
            #* Find walls
            if maps[i][j] == '*':
                walls.append(tuple((i, j)))
            
            #* Find diamonds and diamondScores
            elif maps[i][j] in numbers:
                
                diamond.append(tuple((i, j)))
                
                if maps[i][j] == '0' :
                    green={'name': '0-green', 'position':f'{i},{j}','score':2}
                    diamondSocre.append(green)
                
                elif maps[i][j] == '1' :
                    blue={'name': '1-blue', 'position':f'{i},{j}','score':5}
                    diamondSocre.append(blue)
                
                elif maps[i][j] == '2' :
                    red={'name': '2-red', 'position':f'{i},{j}','score':3}
                    diamondSocre.append(red)
        
                elif maps[i][j] == '3' :
                    yellow={'name': '3-yellow', 'position':f'{i},{j}','score':1}
                    diamondSocre.append(yellow)
                
                elif maps[i][j] == '4' :
                    gray={'name': '4-gary','position':f'{i},{j}','score':10}
                    diamondSocre.append(gray)
            
            #* Find agent position
            elif maps[i][j] == 'A':
                agent = f"{i},{j}"
            
            #* Find homes
            elif maps[i][j] == 'a':
                home.append(f'{i},{j}')

    #* Add edges ==> row
    for i in range(0, len(maps)):
        
        for j in range(0, len(maps)):
            
            if tuple((i, j)) not in walls and tuple((i, j+1)) not in walls:
                
                if j+1 < len(maps):
                    problem.add_edge(f"{i},{j}", f"{i},{j+1}")

    #* Add edges ==> Column
    for j in range(0, len(maps)):
        
        for i in range(0, len(maps)):
            
            if tuple((i, j)) not in walls and tuple((i+1, j)) not in walls:
                
                if i+1 < len(maps):
                    problem.add_edge(f"{i},{j}", f"{i+1},{j}")

    #? Save picture of graph
    nx.draw(problem, with_labels=True)
    plt.savefig("./result/map5/result-map.png")  # save as png #! if run it with consol address ==> from virtualenv
    plt.show()  # display

    return(problem, agent, diamond, diamondSocre, home)

def diamondOrder (problem, agent, diamondScores, homes):
    
    diamond_order = list()          #* To Save order of diamond for each path
    paths = dict()                  #* Return all path for all permutations 
    dict_iterator = 0               #* Key for create dictionary
    paths_cost = 0                  #* Cost of each path
    walk = 0                        #* Number of move for agent
    pointsCollected = 0             #* To calculate score for each path
    turnsLeft = 17                  #! Turns left for agent

    #* List  with all permutations for diamonds
    permutations = it.permutations(diamondScores) 

    #* Cretae path for specific permutation
    for permutation in permutations:

        #* Return path for this specific permutation
        path = whichDiamond(problem, agent, permutation, homes, turnsLeft, walk) 
        
        #* Calculate cost of this path
        for each_path in path: 
            paths_cost += len(each_path)
        
        #* Set order of diamonds for this path
        for diamonds in permutation:  
            diamond_order.append(diamonds.get('name'))

        #* Calculate scores for this path
        length_path = len(path)
        i = 0 
        for diamonds in permutation:
            pointsCollected += diamonds.get('score')
            i+=1
            if i == length_path:
                break
        
        #* cretae dictionary for all path
        paths[f'{dict_iterator}'] = {'path': path, 'order' : diamond_order, 'cost': paths_cost, 'score': pointsCollected} 
        
        # Clear all temp for create other paths
        diamond_order = []
        dict_iterator +=1
        paths_cost = 0
        pointsCollected = 0
    
    return (paths)

def whichDiamond(graph, agent, permutation, homes, turns, walk):
    
    paths = list()          #* Return final path
    each_diamond = list()   #* To save path for each diamond (with home)
    
    for i in range(len(permutation)):
        
        #* Position of diamond
        diamond_position= permutation[i].get('position') 
        
        #* Check for initial state or not!
        if i == 0:
            diamond_path = nx.shortest_path(graph, agent, diamond_position)
        else:
            diamond_path = nx.shortest_path(graph, paths[-1][-1], diamond_position)
        
        #* Add Path for diamonds
        for j in range (1, len(diamond_path)):
            each_diamond.append(diamond_path[j])
        
        #* Find nearest home for diamond
        home_path = whichHome(graph, diamond_position, homes)
        
        #* Add path for home
        for k in range (1, len(home_path)):
            each_diamond.append(home_path[k])
        
        #* Check if our walk more than turns left ==> return last path
        walk += len(each_diamond)
        if walk > turns:
            return paths
        else:
            paths.append(each_diamond)  # each list in paths shows one diamond in home
            each_diamond = []
    
    return (paths)

def whichHome (graph, diamond_pos,homes):
    homePaths = list()  #* All path to all homes in the map 
    homePath = list()  #* Return final home with shortest length
    
    #* All shortest path for all homes
    for home in homes:
        homePaths.append(nx.all_shortest_paths(graph, diamond_pos, home)) 
    
    #* Find shortest path in homes 
    min = 1000
    for each_path in homePaths:
        for path in each_path:
            length = len(path)
            if length < min:
                min = length
                homePath = path
    
    return homePath


with open ('./maps/map5/map.txt' , 'r') as fin:
    problem, agent, diamonds, diamondScores, homes = generateProblem(fin)


with open ('./result/map5/result-map.txt' , 'w') as fin:
    order = diamondOrder(problem,agent,diamondScores,homes)
    fin.writelines(f'{order}\n')
