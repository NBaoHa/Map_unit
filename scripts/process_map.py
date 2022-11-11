import gdal as gd
import ogr
import osr
import cv2
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import planning_algo


class Pathplanning:
    def __init__(self, map_png, facilities_png, weights, ascending_gradient=True, algorithm="A*"):  # smaller pixel size means smoother line results
        # declare parameters
        self.mapdata = []  # initiate not numpy array yet
        self.img = cv2.imread(map_png, 0) # 0 means view as grayscale
        #self.facil_mask = cv2.imread(facilities_png, 0)
        self.weights = weights   # corresponding pixel val to weights
        self.ascending_gradient = ascending_gradient # signify that darker colors have higher weights 
        self.algo = algorithm
        
        # undeclared variables
        self.width, self.height = 0,0  
        self.new_canvas = []   # for accessing canvas --> img[height][width] <-- [y][x]
        self.facility_nodes = {} # store nodes as Hashmap for faster computation
        self.facility_coords = [] # for easier acess in gen map   /// (x, y)
        self.weights_legend = {} # stores cost
        
    def run(self):
        # create new map to store routes
        self.preprocess()
        # place facilities (nodes in graph)
        self.determine_nodes()
        
        
        self.gen_graph()   ## do all possible connections between all the reserves (can filter out later with Network Analysis)

        # show result
        self.show_res()


    def preprocess(self):
        # mark boundaries
        self.width = len(self.img[0])
        self.height = len(self.img)
        print('dimensions: ',self.width, self.height)
        self.new_canvas = [[0]*self.width]*self.height

        # record values in ascending_gradient order (True means small to large, False means otherwise)
        pix_val = [] # 0 is un accountable --> [0, pix1, pix2] --> [0, weight1, weight2]
        for line in self.img:
            for pix in line:
                if pix not in pix_val:
                    pix_val.append(pix)

        if self.ascending_gradient == False:
            pix_val.sort(reverse=True)
            pix_val = pix_val[:-1]
        else:
            pix_val.sort()
            pix_val = pix_val[1:]
        

        #connect weight legend
        self.weights_legend[0] = 999
        for index,uniq_val in enumerate(pix_val):
            self.weights_legend[uniq_val] = self.weights[index]

        print('weight legend: ', self.weights_legend)
       

        
        
        
    def determine_nodes(self):
        '''
        calculate centroids from facilities img and
        place them into new_canvas
        '''
        ### HERE is to calculate centroid coordinates

        ## Draft delete below if the facilities png is available------  !!! can sychronously place facility centroids in blank canvas
        num_facil = 10
        while num_facil > 0:
            smpx, smpy = int(random.uniform(0, self.width)), int(random.uniform(0, self.height))
            while smpx in self.facility_nodes.keys() and smpy in self.facility_nodes[smpx]:
                smpx, smpy = int(random.uniform(0, self.width)), int(random.uniform(0, self.height))
            
            if smpx in self.facility_nodes.keys():
                self.facility_nodes[smpx].append(smpy)
                self.img[smpy][smpx] = 0
                self.facility_coords.append((smpx, smpy))
            else:
                self.facility_nodes[smpx] = [smpy]
                self.facility_coords.append((smpx, smpy))
                self.img[smpy][smpx] = 0

            num_facil -= 1
        ##-----------------------------------------------------------
        print('facilities (x, y): ', self.facility_nodes)
        print('facility coords: ', self.facility_coords)

    def gen_graph(self):
        for c1 in self.facility_coords: # O(n^2)
            for c2 in self.facility_coords:
                if c1 != c2:
                    planning_algo.draw_route(c1, c2, self.img) # self.img is [[pix pix]]
                    break


    def show_res(self):
        cv2.imshow('image', self.img)
        cv2.waitKey(0)




if __name__ == '__main__':
    g = Pathplanning('/home/bao_wy/map_processing_unit/data/Result_700.png',
    'this file contains raster that highlights reserves and hospitals in two different colors but need to be the same dim as the map_png', [1, 2, 3, 4], ascending_gradient=False)
    g.run()
    