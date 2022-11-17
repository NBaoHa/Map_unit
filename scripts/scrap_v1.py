


import cv2
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import math 


def clean_route(c1, c2,route):
    x_y = list(zip(*route))
    max_width = max(x_y[0])
    max_height = max(x_y[1])
    stat_b = np.array([[None]*(max_width+1)]*(max_height+1))
    new_route = [c1]
    cur_pix = c1
    for pix in route:
        x,y = pix
        stat_b[y][x] = 1
    i = 0
    while cur_pix != c2:
        neighbors= add_cand(cur_pix, 0, stat_b)
        cand_index = {}
        for pix in neighbors.keys():
            x, y = pix
            if stat_b[y][x] == 1:
                cand_index[pix] = route.index(pix)
        
        print('connective neighbors',cand_index)
        cur_pix = max(cand_index,key=cand_index.get)
        new_route.append(cur_pix)
        print('next choice',cur_pix)
        if i == 3:
            break
        # i+=1

    new_route.append(cur_pix)  # this is when cur_pix == c2
    print(len(route), len(new_route))
    return new_route

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




if __name__ == "__main__":
    rout = [(185, 11), (186, 11), (186, 12), (187, 13), (186, 13),
             (187, 14), (187, 15), (186, 16), (186, 17), (186, 18), 
             (185, 19), (184, 20), (183, 21), (182, 22), (181, 23), 
             (180, 24), (179, 25), (178, 26), (177, 26), (176, 26),
              (175, 26), (174, 26)]
    g =clean_route((185,11),(176,26),route=rout)
    print(g)
















# def draw_route(c1, c2, map_img, scale_factor=1): # return lst of pixel of optimal route  ### does not mutate map_img
#     '''
#     c1/c2 : (x, y)
#     map_img = [[pix, pix]]

#     '''
#     img = map_img.copy()
#     current = c1
#     end = c2
#     opened = {}
#     closed = {}

#     route = {}
    
#     while current != end:
#         print(current)
#         #img[current[1]][current[0]] = 0  # load marking
#         if closed == {}:
#             closed[current] = 0
#         candidates = add_cand(current, img)

#         if end in candidates:
#             current = end
#             closed[current] = img[end[1]][end[0]]
#             img[current[1]][current[0]]=0
#             break

#         for cand in candidates:
#             if cand not in closed.keys():
#                 x, y = cand
#                 to_target_cost = dst_cords((x, y),c2) * 10000
#                 from_current_cost = dst_cords(c1,(x,y)) * 10000 #change c1 to current if dont want full coverage but c1 is the correct one
#                 criteria_weight = (img[y][x] + 2) * (scale_factor)
#                 opened[cand]= [to_target_cost+from_current_cost+criteria_weight,to_target_cost]
                
#         # choosing between even costs
#         even_cands={}
#         min_choice = min(opened.items(), key=lambda x: x[1][0])   
#         for cand in opened:
#             if opened[cand][0] == min_choice[1][0]:
#                 even_cands[cand] = opened[cand][1]  
#         if len(even_cands) > 1:
#             min_choice = min(even_cands, key=even_cands.get)
#             current = min_choice
#         else:
#             current=min_choice[0]
#         delete_node =opened.pop(current)
#         closed[current]= delete_node
        
#     if current == end:
#         closed[current] = 0
#         img[current[1]][current[0]]=0

#     # choosing best fitted path
#     final_route = []
#     for route_cand in closed.keys():
#         x,y = route_cand
#         route[route_cand] = dst_cords((x, y),end) # addition here should be dist from current node
#         final_route.append(route_cand)
    
    
#     #final_route = BFS(c1, c2, route)

#     # visualization
#     for coord in final_route:
#         img[coord[1]][coord[0]] = 0
#     plt.imshow(img)
#     plt.scatter([c1[0], c2[0]], [c1[1],c2[1]],c='r', marker=">")
#     plt.show()

#     return final_route

#     ###visualization and return
    


    
    
# def BFS(c1, c2, route_dict):
#     #memory visisted node manager
#     coords_unzip = list(zip(*route_dict.keys()))
#     max_width, max_height = max(coords_unzip[0]), max(coords_unzip[1])
#     #print(max_width, max_height)
#     status_b =np.array([[None]*(max_width+1)]*(max_height+1))
    
#     # initiate starting node
#     current = c1
#     prev=current
#     status_b[c1[1]][c1[0]] = 0
#     n_route = [current]
    
#     while current != c2:
#         candidates = collect_cand(current, route_dict)
#         available_cands = []
#         #print('candidates:',candidates)
#         for cand in candidates:
#             x,y = cand
#             if status_b[y][x] == None:
#                 available_cands.append(cand)
#                 #print('avail_cands',available_cands)
        
#         if len(available_cands) == 0:
#             #print('no cands')
#             status_b[current[1]][current[0]] = 1
#             current = n_route[-1]
        
#         else:  # if there is available cands
#             next_choice = available_cands[0]
#             min_cost = route_dict[available_cands[0]] + dst_cords(current,available_cands[0])
#             for cand in available_cands:
#                 x,y = cand
#                 cost = dst_cords(current, cand) + route_dict[cand]
#                 if cost < min_cost:
#                     next_choice = cand
#                     min_cost = cost
            
#             current = next_choice
#             n_route.append(current)
#             status_b[current[1]][current[0]] = 0
#     # final_rt = clean_route(n_route)
#     # return final_rt
#     return n_route
        
# def clean_route(route):
#     # new_route=[]
#     # cur_pointer = route[0]
#     # cur_compare = route[0]
#     # while cur_pointer != route[-1]:
#     #     if cur_pointer
#     new_route = []
#     for index,compared in enumerate(route):
#         for index2,candidate in enumerate(route):
#             pass






# def collect_cand(c1, route):
#     '''
#     only aggregate existing route candidates to current node
#     '''
#     cands = []
#     for pix in route.keys():
#         x,y= pix
#         x_or,y_or = c1
#         if (x == x_or +1 and y == y_or) or (x==x_or-1 and y == y_or) or \
#             (y==y_or+1 and x==x_or) or (y==y_or-1 and x==x_or) or \
#                 (x== x_or+1 and y==y_or+1) or (x == x_or+1 and y==y_or-1) or \
#                     (x== x_or-1 and y==y_or+1) or (x == x_or-1 and y==y_or-1):
#                     cands.append(pix)

#     return cands

# def add_cand(c1, img):
#     width = len(img[0])
#     height = len(img)
 
#     candidates = []
#     x,y = c1[0], c1[1]
#     if x > 0:
#         if img[y][x-1] !=0:
#             candidates.append((x-1, y))
#         if y > 0 and img[y-1][x-1] != 0:
#             candidates.append((x-1, y-1)) # top left pixel
#         if y < height -1 and img[y+1][x-1]:
#             candidates.append((x-1,y+1)) # bottom left pixel

#     if x < width-1:
#         if img[y][x+1] !=0:
#             candidates.append((x+1, y))
#         if y > 0 and img[y-1][x+1] != 0:
#             candidates.append((x+1, y-1)) # top right pixel
#         if y < height-1 and img[y+1][x+1] !=0:
#             candidates.append((x+1, y+1))
#     if y > 0:
#         if img[y-1][x] !=0:
#             candidates.append((x, y-1))
#     if y < height-1:
#         if img[y+1][x] !=0:
#             candidates.append((x, y+1))
#     return candidates

# def dst_cords(c1, c2):
#     x_dist = abs(c2[0] - c1[0])
#     y_dist = abs(c2[1]- c2[1])
#     dist = math.sqrt(x_dist**2 + y_dist**2)
#     return dist

# if __name__ == "__main__":
#     # img = [list(np.random.randint(low = 1,high=5,size=50))]
#     # while len(img) < 51:
#     #     img.append(list(np.random.randint(low = 1,high=5,size=50)))
#     # print(img)
#     img = [[4, 1, 3, 4, 2, 3, 4, 0, 0, 0],
#            [3, 1, 3, 5, 7, 9, 1, 3, 2, 3], 
#            [1, 3, 2, 1, 4, 2, 2, 2, 1, 3], 
#            [2, 1, 1, 4, 3, 4, 4, 8, 9, 4], 
#            [10, 1, 3, 2, 2, 2, 1, 1, 1, 2], 
#            [5, 10, 10, 9, 1, 1, 1, 1, 2, 2], 
#            [0, 0, 2, 11, 8, 1, 1, 1, 1, 4], 
#            [0, 0, 0, 3, 7, 1, 4, 3, 3, 4]]

#     #image = cv2.imread('/home/bao/Map_unit/Map_unit/data/Result_700.png', 0)
#     #print(img)
#     plt.imshow(img)
#     plt.show()
#     route = draw_route((1, 0), (8,6), img)#[:100])
#     print(route)
