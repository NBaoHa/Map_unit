import gdal as gd
import ogr
import osr
import cv2
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt



def draw_route(c1, c2, map_img): # return lst of pixel of optimal route  ### does not mutate map_img
    '''
    c1/c2 : (x, y)
    map_img = [[pix, pix]]

    '''
    img = map_img.copy()
    current = c1
    end = c2
    route = [c1]
    
    while current != end:
        candidates = get_cand(current, img) # top, down, left, right pixel
        print(candidates)
        
        min_cost = lean_dir(c1, c2, candidates)

        #do comparison here (if all are not same weight)

        current = candidates[min_cost][0]
        route.append(current)
        img[current[1]][current[0]] = None
        print(route)


def get_cand(coord, img_array):
    cand = {
        'top': None, 
        'down': None, 
        'left': None, 
        'right': None, 
    }
    height_y = len(img_array)
    width_x = len(img_array[0])
    print(height_y, width_x)
    x, y = coord[0], coord[1]
    if x > 0:    
        cand['left'] = [(x-1, y),img_array[y][x-1]]
    
    if x < width_x-1:
        cand['right'] = [(x + 1, y),img_array[y][x+1]]
    
    if y > 0:
        cand['top'] = [(x, y-1),img_array[y-1][x]]
    
    if y < height_y-1:
        cand['down'] = [(x, y + 1),img_array[y+1][x]]

    return cand


def lean_dir(coord1, coord2, candidates:dict):
    '''
    in case where all candidates have equal weights, 
    choose the one that leads toward goal
    '''
    choice = []
    if coord1[0] < coord2[0] and candidates['right']!= None:
        choice.append('right')
    elif coord1[0] > coord2[0] and candidates['left'] != None:
        choice.append('left')
    
    if coord1[1] < coord2[1] and candidates['down'] != None:
        choice.append('down')
    elif coord1[1] > coord2[1] and candidates['top'] != None:
        choice.append('top')
    
    rand_choice = int(random.uniform(0, len(choice)-1))
    return choice[rand_choice]




if __name__ == "__main__":
    img = [[0, 2, 3, 4, 5, 6, 7, 8, 9],
           [1, 0, 2, 3, 4, 1, 1, 5, 6],
           [1, 0, 2, 3, 4, 1, 1, 5, 6],
           [1, 3, 2, 3, 4, 1, 1, 5, 6],
           [1, 1, 2, 3, 4, 1, 1, 5, 6],
           [1, 3, 2, 3, 4, 1, 1, 5, 6],
           [1, 6, 2, 3, 4, 1, 1, 5, 6],
           [1, 4, 2, 3, 4, 1, 1, 5, 6]]

    start = (0, 0)
    end = (7, 6)

    draw_route(start, end, img)