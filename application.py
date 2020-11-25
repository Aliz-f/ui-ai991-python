import networkx as nx
import matplotlib.pyplot as plt 

def generateGraph():
    G=nx.Graph() #Create Graph
    maps = list() #List for Maps
    walls = list() #List for locations Walls 
    diamond = list() #List for Location diamond
    home = list() #Lisr fot location Homes
    numbers = ["0","1","2","3","4"]
    with open("Maps/map3/map.txt" , "r") as fin:

        for line in fin:
            maps.append(list(line.strip()))
        
        for i in range(0 , len(maps)):
            for j in range(0 , len(maps)):
                if maps[i][j] == '*':
                    walls.append(tuple((i,j)))
                elif maps[i][j] in numbers:
                    diamond.append(tuple((i,j)))
                elif maps[i][j] == 'A':
                    agent = tuple((i,j))
                elif maps[i][j] == 'a':
                    home.append(tuple((i,j)))

        for i in range (0 , len(maps)):
            for j in range (0 , len(maps)):
                if tuple((i,j)) not in walls and tuple((i,j+1)) not in walls:
                    if j+1 < len(maps):
                        G.add_edge(f"{i},{j}",f"{i},{j+1}")
        
        for j in range (0 , len(maps)):
            for i in range (0 , len(maps)):
                if tuple((i,j)) not in walls and tuple((i+1,j)) not in walls:
                    if i+1 < len(maps):
                        G.add_edge(f"{i},{j}",f"{i+1},{j}")

    nx.draw(G,with_labels=True)
    plt.savefig("test.png") # save as png
    plt.show() # display
                    


    # print('walls: ',walls)
    # print('diamond: ',diamond)
    # print('agent: ',agent)
    # print('home: ',home)

generateGraph()