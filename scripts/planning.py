import cv2
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import math 


######  A* path planning algorithm
def draw_route(c1, c2, map_img, scale_factor=1): # return lst of pixel of optimal route  ### does not mutate map_img
    '''
    c1/c2 : (x, y)
    map_img = [[pix, pix]]

    '''
    img = map_img.copy()
    current = [c1,0]  # initiate cost
    end = c2
    opened = []
    closed = [current[0]]
    closed_cost =[current[1]]
    terminated=[] # stores leaf nodes that are from lost branch
    
    while current[0] != c2:
        x, y = current[0]
        print('current',current[0])
        neighbors = add_cand(current[0], current[1], img)  # {(x,y):from_cost}
        ###############print('all neighbors', neighbors)

        # check for open neighbors
        available_neighbors = {}
        for n in neighbors:
            if n not in closed and n not in terminated:
                xn,yn=n
                available_neighbors[n] = dst_cords(n,end) + (img[yn][xn]*scale_factor)
                opened.append(n)
        ################print('opened',opened)
        ################print('available',available_neighbors)


        #### if current is the lost branch (leads to nowhere) --> current becomes previous
        if len(available_neighbors) == 0:
            print('tr')
            closed.remove(current[0])
            terminated.append(current[0])
            current=[closed[-1],closed_cost[-1]]
            
        
        else:

            ## breaking ties
            min_coord = min(available_neighbors, key=available_neighbors.get)
            min_cost = available_neighbors[min_coord]
            #####################print('min_cost', min_cost)
            ties = []
            for n in available_neighbors:
                if available_neighbors[n] == min_cost:
                    ties.append(n)
            ################print('ties', ties)

            # if to target is the same cost, check for from target cost
            if len(ties) > 1:  
                choice = ties[0]
                cost = neighbors[choice]
                for n in ties:
                    if neighbors[n] < cost:
                        choice = n
                        cost = neighbors[n]
                current = [choice, neighbors[choice]] 
                
            else:  # no ties
                current = [min_coord,neighbors[min_coord]]
            
            opened.remove(current[0])
            closed.append(current[0])
            closed_cost.append(current[1])

            print(current)

        
    ##################print('closed',closed)
        
    ## visualize:
    for coord in closed:
        x,y= coord
        img[y][x] = 0
    
    plt.imshow(img)
    plt.scatter([c1[0], c2[0]], [c1[1],c2[1]],c='r', marker=">")
    plt.show()
    return closed

    
def add_cand(c1, cost, img):
    width = len(img[0])
    height = len(img)
 
    candidates = {}
    x,y = c1[0], c1[1]
    if x > 0:
        if img[y][x-1] !=0:
            candidates[(x-1, y)] = cost+ 10
        if y > 0 and img[y-1][x-1] != 0:
            candidates[(x-1, y-1)]=cost+14 # top left pixel
        if y < height -1 and img[y+1][x-1]:
            candidates[(x-1,y+1)]=cost+14 # bottom left pixel

    if x < width-1:
        if img[y][x+1] !=0:
            candidates[(x+1, y)]=cost+10
        if y > 0 and img[y-1][x+1] != 0:
            candidates[(x+1, y-1)]=cost+14 # top right pixel
        if y < height-1 and img[y+1][x+1] !=0:
            candidates[(x+1, y+1)] = cost+14 #bottom right pixel
    if y > 0:
        if img[y-1][x] !=0:
            candidates[(x, y-1)]=cost+10
    if y < height-1:
        if img[y+1][x] !=0:
            candidates[(x, y+1)]=cost+10
    return candidates

def dst_cords(c1, c2):
    x_dist = abs(c2[0] - c1[0])
    y_dist = abs(c2[1]- c1[1])
    dist = math.sqrt(x_dist**2 + y_dist**2)
    return dist

if __name__ == "__main__":
    # img = [list(np.random.randint(low = 1,high=5,size=50))]
    # while len(img) < 51:
    #     img.append(list(np.random.randint(low = 1,high=5,size=50)))
    # print(img)
    img = [[4, 1, 3, 4, 2, 3, 4, 0, 0, 0],
           [3, 1, 3, 5, 7, 9, 1, 3, 2, 3], 
           [1, 3, 2, 1, 4, 2, 2, 2, 1, 3], 
           [2, 1, 1, 4, 3, 4, 4, 8, 9, 4], 
           [10, 1, 3, 2, 2, 2, 1, 1, 1, 2], 
           [5, 10, 10, 9, 1, 1, 1, 1, 2, 2], 
           [0, 0, 2, 11, 8, 1, 1, 1, 1, 4], 
           [0, 0, 0, 3, 7, 1, 4, 3, 3, 4]]

    #image = cv2.imread('/home/bao/Map_unit/Map_unit/data/Result_700.png', 0)
    #print(img)
    plt.imshow(img)
    plt.show()
    route = draw_route((1, 0), (8,6), img)#[:100])
    #print(route)
