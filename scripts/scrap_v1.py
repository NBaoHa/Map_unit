import matplotlib.pyplot as plt
import cv2

img ='/Users/baoha/Desktop/Pathplanning/Map_unit/data/Result_500.png'

image = cv2.imread(img, 0)
print(image)

pixels = {}
for line in image:
    for pix in line:
        if pix in pixels.keys():
            pixels[pix] +=1
        else:
            pixels[pix] = 1

print(pixels)


        



plt.imshow(image)
plt.show()


