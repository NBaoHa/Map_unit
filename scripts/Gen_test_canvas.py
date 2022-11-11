import cv2
from osgeo import gdal,ogr,osr
import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.plot import show
import random


# parameters
length = 100
width = 80
max_pxl = length * width
gen_img = []
probability = [80, 0, 10, 5, 4, 1]  # must add up to 100
weights = [0, 1, 2, 3, 4, 5]

# assigning number of pixels for the weightsbased on percentage
pixels ={
    0: probability[0]*max_pxl/100,
    1: probability[1]*max_pxl/100,
    2: probability[2]*max_pxl/100,
    3: probability[3]*max_pxl/100,
    4: probability[4]*max_pxl/100,
    5: probability[5]*max_pxl/100
}
print(pixels)
# initiating blank canvas
canvas = np.asarray([[weights[-1]+5]*width]*length) # [length][width] --> [y][x]  "weights[-1]+5" will be see as NULL values that is Int type
tracking_canvas = np.asarray([[0]*width]*length)
print(f"length: {len(canvas)}, width: {len(canvas[0])}")



# scatter pixel weights across canvas

# stores coordinates that existed already
occupied = {} #  usage of hashmaps (buckets) to speed up computational time
sp_x, sp_y = 0,0
percentage = 0

#scatter plot purposes
x_arr, y_arr, hght = [], [], []


for weight in weights:
    print(weight, pixels[weight])
    npix = pixels[weight]
    while npix > 0:
        print(f"remaining pixels: {npix}")
        while (canvas[sp_y][sp_x] != weights[-1]+5):
            sp_x, sp_y =int(random.uniform(0, width)), int(random.uniform(0, length))
      
        
        #scatter plot purposes
        x_arr.append(sp_x)
        y_arr.append(sp_y)
        hght.append(weight)

        #apply weights to blank space
        canvas[sp_y][sp_x] = weight
        npix -= 1
    


print(canvas)
        
    
# img = np.array(gen_img)


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x_arr, y_arr, hght, c='r', marker='o')
# plt.show()
file = open("/home/bao/mapp_processing_Unit/data/output.txt", "w")

for line in canvas:
    string = ""
    for pix in line:
        string = string+f"{pix} "
    string = string + "\n"
    file.write(string)

file.close()
plt.figure()
plt.imshow(canvas)
plt.colorbar()
plt.show()


######
lst = facilities = {
    'hospital': [(40, 10), (677, 40), (500, 23), (412, 482)]
}