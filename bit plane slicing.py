#bit plane slicing 
import cv2 
import numpy as np
import matplotlib.pyplot as plt

#from google.colab.patches import cv2_imshow

img = cv2.imread('/content/drive/My Drive/standard_test_images/lena_color_256.tif',0) 

out = {}

for k in range(0, 8):
    # create an image for each k bit plane
    plane=np.zeros((img.shape[0],img.shape[1]),np.uint8)
    # execute bitwise and operation
    for i in range(img.shape[0]):
    	for j in range(img.shape[1]):
    		plane[i,j]=img[i,j] & (1<<k)
    #save each sliced image in a dictionary
    out[f'bp{k}']=plane
i=1
plt.figure(figsize=(30,30))
for key in out:
    plt.subplot(1,8,i)
    plt.imshow(out[key],cmap='gray')
    plt.title(key,fontsize=40)
    plt.xticks([])
    plt.yticks([])
    i+=1

plt.show()