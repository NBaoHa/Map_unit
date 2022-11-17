
import cv2
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import planning


class Pathplanning:
    def __init__(self, map_png, facilities_png, ascending_gradient=True, algorithm="Dijkstra"):  # smaller pixel size means smoother line results  # dijkstra for computational purposes
        # declare parameters
        self.mapdata = []  # initiate not numpy array yet
        self.img = cv2.imread(map_png, 0) # 0 means view as grayscale
        self.img = self.img
        self.facil_mask = cv2.imread(facilities_png, 0)
        self.weights = []   # corresponding pixel val to weights
        self.ascending_gradient = ascending_gradient # signify that darker colors have higher weights 
        self.algo = algorithm
        
        # undeclared variables
        self.width, self.height = 0,0  
        self.new_canvas = []   # for accessing canvas --> img[height][width] <-- [y][x]
        self.facility_nodes = {} # store nodes as Hashmap for faster computation
        self.facility_coords = [] # for easier acess in gen map   /// (x, y)
        self.weights_legend = {} # stores cost

        #output variables
        self.routes = {}
        
    def run(self):
        # create new map to store routes
        self.preprocess()
        # place facilities (nodes in graph)
        self.determine_nodes()
        
        
        self.gen_graph()   ## do all possible connections between all the reserves (can filter out later with Network Analysis)
        #print(self.routes.keys())
        # show result

        #self.gen_new_img()
        #self.show_res()


    def preprocess(self):
        # mark boundaries
        self.width = len(self.img[0])
        self.height = len(self.img)
        print(self.img)
        # print(len(self.facil_mask[0]))  ## make sure two png are the same dim
        # print(len(self.facil_mask))
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
        
        
        self.weights = list(range(1,len(pix_val)+1))
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
        # curx,cury = 0,0
        # temp_coord = []
        # x_arr = []
        # y_arr = []
        # while cury < self.height:
        #     while curx < self.width:
        #         if self.facil_mask[cury][curx] == 255:
        #             self.facil_mask[cury][curx] = 100
        #             x_arr.append(curx)
        #             y_arr.append(cury)
        #             temp_coord.append((curx, cury))
                
        #         curx +=1
        #     curx =0
        #     cury+=1

            ## get centroid

        
        
        # xlang,ylang = x_arr,y_arr

        # print(temp_coord)
        # plt.imshow(self.img)
        # plt.imshow(self.facil_mask)
        # plt.scatter(xlang, ylang, c='r', marker=">")
        # plt.show()
        
        #print(self.facil_mask[300:400][0])
        ## Draft delete below if the facilities png is available------  !!! can sychronously place facility centroids in blank canvas
        # num_facil = 2
        # while num_facil > 0:
        #     smpx, smpy = int(random.uniform(0, self.width)), int(random.uniform(0, self.height))
        #     while smpx in self.facility_nodes.keys() and smpy in self.facility_nodes[smpx]:
        #         smpx, smpy = int(random.uniform(0, self.width)), int(random.uniform(0, self.height))
            
        #     if smpx in self.facility_nodes.keys():
        #         self.facility_nodes[smpx].append(smpy)
        #         self.img[smpy][smpx] = 0
        #         self.facility_coords.append((smpx, smpy))
        #     else:
        #         self.facility_nodes[smpx] = [smpy]
        #         self.facility_coords.append((smpx, smpy))
        #         self.img[smpy][smpx] = 0

        #     num_facil -= 1
        ##-----------------------------------------------------------
        self.facility_coords=[(100, 300), (20, 200), (170, 12)]
        print('facilities (x, y): ', self.facility_nodes)
        print('facility coords: ', self.facility_coords)
        

    def gen_graph(self):
        for c1 in self.facility_coords: # O(n^2)
            for c2 in self.facility_coords:
                if c1 != c2 and ((c2, c1) not in self.routes.keys()):
                    #print(self.img[c1[1]][c1[0]])
                    # if self.img[c1[1]][c1[0]] != 0 and self.img[c2[1]][c2[0]] != 0:
                    route = planning.draw_route(c1, c2, self.img) # self.img is [[pix pix]]
                    print(route)
                    self.routes[(c1,c2)] = route

    def gen_new_img(self):
        for route in self.routes:
            for coord in self.routes[route]:
                x,y = coord[0], coord[1]
                self.img[y][x] = 0


                


    def show_res(self):
        cv2.imshow('image', self.img)
        cv2.imshow("mask",self.facil_mask)
        cv2.waitKey(0)




if __name__ == '__main__':
    g = Pathplanning('/Users/baoha/Desktop/Pathplanning/Map_unit/data/asdff.png',
    '/Users/baoha/Desktop/Pathplanning/Map_unit/data/reserves_700.png', ascending_gradient=False)
    g.run()
    