
import cv2
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import math 



def draw_route(c1, c2, map_img, scale_factor=10): # return lst of pixel of optimal route  ### does not mutate map_img
    '''
    c1/c2 : (x, y)
    map_img = [[pix, pix]]

    '''
    img = map_img.copy()
    current = c1
    end = c2
    cost = {}
    opened = {}
    closed = {}
    
    
    while current != end:
        #print(current)
        img[current[1]][current[0]] = 0
        if closed == {}:
            closed[current] = 0
        candidates = add_cand(current, img)


        if end in candidates:
            current = end
            closed[current] = img[end[1]][end[0]]
            img[current[1]][current[0]]=0
            break

        even_compare = {}
        for cand in candidates:
            if cand not in closed.keys():
                x, y = cand
                to_target_cost = dst_cords((x, y),end) * 10
                from_current_cost = dst_cords(c1,(x,y)) * 10 #change c1 to current if dont want full coverage but c1 is the correct one
                criteria_weight = img[y][x] * (scale_factor)
                opened[cand]= [to_target_cost+from_current_cost+criteria_weight,to_target_cost]
                

        
        even_cands={}
        min_choice = min(opened.items(), key=lambda x: x[1][0]) 
        
        for cand in opened:
            if opened[cand][0] == min_choice[1][0]:
                even_cands[cand] = opened[cand][1] 
        
        if len(even_cands) > 1:
            min_choice = min(even_cands, key=even_cands.get)
            print(min_choice)
            current = min_choice
        else:
            current=min_choice[0]

        delete_node =opened.pop(current)
        closed[current]= delete_node
        
    
    if current == end:
        closed[current] = 0
        img[current[1]][current[0]]=0

    plt.imshow(img)
    plt.scatter([c1[0], c2[0]], [c1[1],c2[1]],c='r', marker=">")
    plt.show()
    return closed.keys()

    # go one node and access the next by comparing weights (refurbish path plan)
    
    


def add_cand(c1, img):
    width = len(img[0])
    height = len(img)
 
    candidates = []
    x,y = c1[0], c1[1]
    if x > 0:
        if img[y][x-1] !=0:
            candidates.append((x-1, y))
        if y > 0 and img[y-1][x-1] != 0:
            candidates.append((x-1, y-1)) # top left pixel
        if y < height -1 and img[y+1][x-1]:
            candidates.append((x-1,y+1)) # bottom left pixel

    if x < width-1:
        if img[y][x+1] !=0:
            candidates.append((x+1, y))
        if y > 0 and img[y-1][x+1] != 0:
            candidates.append((x+1, y-1)) # top right pixel
        if y < height-1 and img[y+1][x+1] !=0:
            candidates.append((x+1, y+1))
    if y > 0:
        if img[y-1][x] !=0:
            candidates.append((x, y-1))
    if y < height-1:
        if img[y+1][x] !=0:
            candidates.append((x, y+1))
    return candidates

def dst_cords(c1, c2):
    x_dist = abs(c2[0] - c1[0])
    y_dist = abs(c2[1]- c2[1])
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

    image = cv2.imread('/home/bao/Map_unit/Map_unit/data/Result_700.png', 0)
    print(image[:100])
    plt.imshow(image)#[:100])
    plt.show()
    draw_route((150, 300), (450,450), image)#[:100])