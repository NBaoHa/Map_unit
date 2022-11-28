from sklearn.cluster import KMeans
import cv2
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import planning
import sys

class Pathplanning:
    def __init__(self, map_png, facilities_png,output_file, ascending_gradient=True, scale_factor=10):  # smaller pixel size means smoother line results  # dijkstra for computational purposes
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
        self.scale_factor = scale_factor
        self.output_file = output_file

        # undeclared variables
        self.width, self.height = 0,0  
        self.new_canvas = []   # for accessing canvas --> img[height][width] <-- [y][x]
        self.facility_nodes = {} # store nodes as Hashmap for faster computation
        self.facility_coords = [] # for easier acess in gen map   /// (x, y)
        self.weights_legend = {} # stores cost
        self.facilities_arr = {'x':[], 'y':[]} # for plotting
        self.routes = {}
        
    def run(self):
        # create new map to store routes
        self.preprocess()
        # place facilities (nodes in graph)
        self.determine_nodes()
        # generate routes between facilities
        self.gen_graph()  
        # generate new image with routes
        self.gen_new_img()
        self.show_res()
        # export routes to png using cv2
        self.export_routes()



    def preprocess(self):
        # mark boundaries
        self.width = len(self.img[0])
        self.height = len(self.img)
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
        self.weights_legend[0] = max(self.weights)+1
        for index,uniq_val in enumerate(pix_val):
            self.weights_legend[uniq_val] = self.weights[index]

        print('weight legend: ', self.weights_legend)

        #create new imagery with re-evaluated weights
        for y, x in np.ndindex(self.img.shape):
            key_val = self.img[y][x]
            self.new_canvas[y][x] = self.weights_legend[key_val]
            
        print('new canvas: ', self.new_canvas)
        
       

        
        
        
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

        # manually place facilities if no facility image is given
        else:
            plt.imshow(self.new_canvas, cmap='gray')#,cmap='gray')
            plt.show()
            print('no facilities png provided, manually place facilities')
            print(f'Please place facilities on the map within the boundaries of {self.width} and {self.height}')
            facilities = (input('what are the facilities coordinates? (x,y)')).split(' ')
            for facility in facilities:
                x,y = facility.split(',')
                self.facility_coords.append((int(x),int(y)))
                self.facilities_arr['x'].append(int(x))
                self.facilities_arr['y'].append(int(y))
            print('facility coords: ', self.facility_coords)
        

    def gen_graph(self):
        tag= 0
        amount = 1
        output = len(self.facility_coords)* (len(self.facility_coords)-1)
        for c1 in self.facility_coords: # O(n^2)
            for c2 in self.facility_coords:
                if c1 != c2 and ((c2, c1) not in self.routes.keys()):
                    
                    route = planning.draw_route(c1, c2, self.new_canvas, scale_factor=self.scale_factor,Null_factor=self.weights_legend[0]) # self.img is [[pix pix]]
                    print(f'{int(amount / output * 100)}% done')
                    #print(route)
                    self.routes[tag] = route
                    tag += 1
                    amount +=1

    def gen_new_img(self):
        # create new image with routes
        for y, x in np.ndindex(self.new_canvas.shape):
            key_val = self.new_canvas[y][x]
            if key_val == self.weights_legend[0]:
                self.new_canvas[y][x] = 0
                
            else:
                self.new_canvas[y][x] +=50 

        interval = 255
        for route_tag in self.routes:
            for coord in self.routes[route_tag]:
                x,y = coord[0], coord[1]
                self.new_canvas[y][x] = interval # to separate different routes
                self.img[y][x] = 150
            interval -=0
        
        

    def export_routes(self):
        # export routes to png using cv2
        cv2.imwrite(self.output_file, self.new_canvas)
        print(f'exported routes to {self.output_file}')
       
        

        
    def show_res(self):
        # print origin image would be nice bonus
        plt.imshow(self.new_canvas, cmap='gray')
        #plt.imshow(self.img, cmap='gray')
        #scatter plot facilities
        plt.scatter(self.facilities_arr['x'], self.facilities_arr['y'], c='r', marker='>')
        plt.show()




if __name__ == '__main__':
    g = Pathplanning(
        '/Users/baoha/Desktop/Pathplanning/Map_unit/data/Result_300.png',
        '',
        '/Users/baoha/Desktop/Pathplanning/Map_unit/data/path_planned_res_sc20_300.png',
        ascending_gradient=True,
        scale_factor=20)
    g.run()
    