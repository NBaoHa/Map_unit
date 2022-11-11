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
    while not covered(img):
        current = c1
        while current != end:
            pass

def covered(img):
    for line in img:
        for pix in line:
            if pix != 999:
                return False
    return True