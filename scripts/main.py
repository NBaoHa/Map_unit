
import matplotlib.pyplot as plt
import numpy as np




fin = open('/home/bao/mapp_processing_Unit/data/output.txt', "r")
img =[]

for line in fin.readlines():
    new_lst = map(lambda a: int(a), line.split())
    new_lst =list(new_lst)
    img.append(new_lst)

img = np.asarray(img)




lst_facilities = {
    'hospital': ([(40, 10), (67, 40), (50, 23), (41, 48)],'r')
}

for key in lst_facilities:
    for coord in lst_facilities[key][0]:
        img[coord[1], coord[0]] = 8



print(img)
plt.figure()
plt.imshow(img)
plt.colorbar()
plt.show()