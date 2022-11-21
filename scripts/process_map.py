from sklearn.cluster import KMeans
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
        self.img = np.array(self.img)
        if facilities_png == "": # if no facilities png is provided, then manually place facilities
            self.facil_mask = None
        else:
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
        self.facilities_arr = {'x':[], 'y':[]} # for plotting

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

        self.gen_new_img()
        self.show_res()


    def preprocess(self):
        # mark boundaries
        self.width = len(self.img[0])
        self.height = len(self.img)
        print(self.img)
        # print(len(self.facil_mask[0]))  ## make sure two png are the same dim
        # print(len(self.facil_mask))
        print('dimensions: ',self.width, self.height)
        self.new_canvas = [[0]*self.width]*self.height
        self.new_canvas = np.array(self.new_canvas)

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
        print(f'max_pix_val {max(self.weights)}')
        self.weights_legend[0] = max(self.weights)+5
        for index,uniq_val in enumerate(pix_val):
            self.weights_legend[uniq_val] = self.weights[index]

        print('weight legend: ', self.weights_legend)

        #create new imagery with re-evaluated weights
        
        for y, x in np.ndindex(self.img.shape):
            key_val = self.img[y][x]
            self.new_canvas[y][x] = self.weights_legend[key_val]
            
            
        
       

        
        
        
    def determine_nodes(self):
        '''
        calculate centroids from facilities img and
        place them into new_canvas
        '''
        ''' cluster pixels with value of 255 in self.facil_mask into centroids'''
        if self.facil_mask is not None:
            # find all the pixels with value of 255
            for y in range(len(self.facil_mask)):
                for x in range(len(self.facil_mask[0])):
                    if self.facil_mask[y][x] == 255:
                        self.facility_coords.append((x,y))
            plt.imshow(self.facil_mask)
            plt.show()

            # cluster all points in self.facility_coords into centroids (using k-means) 
            kmeans = KMeans(n_clusters=10, random_state=0).fit(self.facility_coords)
            centroids = kmeans.cluster_centers_
            print('centroids: ', centroids)
            #round centroids to nearest int and store in self.facility_coords
            self.facility_coords = []

            # go through all coordinates in self.facility_coords and change the pixel value in self.facilmask to 255 on those coordinates while other pixels are 0
            for coord in centroids:
                x,y = int(coord[0]), int(coord[1])
                self.facility_coords.append((x,y))
            
            print('facility coords: ', self.facility_coords)
            #for each coordinate in self.facility_coords, put x,y into self.facility_arr    
            for coord in self.facility_coords:
                x,y = coord[0], coord[1]
                self.facilities_arr['x'].append(x)
                self.facilities_arr['y'].append(y)

        else:
            # manually place facilities
            plt.imshow(self.new_canvas)#,cmap='gray')
            plt.show()
            print(f'Please place facilities on the map within the boundaries of {self.width} and {self.height}')
            facilities = (input('what are the facilities coordinates? (x,y)')).split(' ')
            for facility in facilities:
                x,y = facility.split(',')
                self.facility_coords.append((int(x),int(y)))
                self.facilities_arr['x'].append(int(x))
                self.facilities_arr['y'].append(int(y))
            print('facility coords: ', self.facility_coords)
        

    def gen_graph(self):
        for c1 in self.facility_coords: # O(n^2)
            for c2 in self.facility_coords:
                if c1 != c2 and ((c2, c1) not in self.routes.keys()):
                    
                    route = planning.draw_route(c1, c2, self.new_canvas) # self.img is [[pix pix]]
                    
                    #print(route)
                    self.routes[(c1,c2)] = route

    def gen_new_img(self):
        for route in self.routes:
            for coord in self.routes[route]:
                x,y = coord[0], coord[1]
                self.new_canvas[y][x] = 10


                


    def show_res(self):
        # print origin image would be nice bonus
        plt.imshow(self.new_canvas)
        #scatter plot facilities
        plt.scatter(self.facilities_arr['x'], self.facilities_arr['y'], c='r', marker='>')
        plt.show()





if __name__ == '__main__':
    g = Pathplanning('/Users/baoha/Desktop/Pathplanning/Map_unit/data/Result_500.png',
    '', ascending_gradient=False)
    g.run()
    