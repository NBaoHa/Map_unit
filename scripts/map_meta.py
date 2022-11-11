import gdal as gd
import ogr
import osr
import cv2
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

img_int = cv2.imread('/home/bao_wy/map_processing_unit/data/Result_700.png', 0) #cv2.IMREAD_UNCHANGED)
# scale_percent = 300 # percent of original size
# width = int(img_int.shape[1] * scale_percent / 100)
# height = int(img_int.shape[0] * scale_percent / 100)
# dim = (width, height)
  
# resize image
# img_blur = cv2.resize(img_int, dim, interpolation = cv2.INTER_AREA)
# cv2.imshow('image',img)
# cv2.waitKey()
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img_blur = cv2.GaussianBlur(img, (5,5), 0) 

#img_blur = cv2.medianBlur(img,1) 

# sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
# sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
# sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) 


cv2.imshow('image',img_int)
cv2.waitKey(0)


# cv2.imshow('Sobel X', sobelx)
# cv2.waitKey(0)
# cv2.imshow('Sobel Y', sobely)
# cv2.waitKey(0)
# cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
# cv2.waitKey(0)
 
# edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
# cv2.imshow('Canny Edge Detection', edges)
# cv2.waitKey(0)
 
# cv2.destroyAllWindows()

########################
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

# pixel_values = img_blur.reshape((-1, 3))
# pixel_values = np.float32(pixel_values)
# print(pixel_values)
# k = 3
# _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# centers = np.uint8(centers)

# labels = labels.flatten()

# segmented_image = centers[labels.flatten()]
# segmented_image = segmented_image.reshape(img_blur.shape)

# plt.imshow(segmented_image)
# plt.show()

# img_blur = img_blur[...,::-1]

# img_changed =[]
# for line in img_blur:
#     print(line)
#     l = []
#     for p in line:
#         if p[0] > 255:
#             if p[1] < 100:
#                 l.append([0,0,0])
#         else:
#             l.append(p)
#     img_changed.append(l)

# print(img_changed)




# plt.imshow(img_changed)
# plt.show()