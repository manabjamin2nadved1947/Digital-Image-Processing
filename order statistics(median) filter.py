# median filter non-linear spatial filter
import cv2
import urllib
import numpy as np

#req = urllib.request.urlopen('/content/drive/MyDrive/standard_test_images/IMG20220501224942 (1).jpg')
#arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#img = cv2.imdecode(arr, 0) 

img= cv2.imread('/content/drive/MyDrive/standard_test_images/microchip.png',0)
height,width = img.shape
padded=np.pad(img,((1,1),(1,1)),'constant')

median=np.zeros((height,width),np.uint8)

k_h,k_w=3,3

for i in range(1,height+1):
    for j in range(1,width+1):
        a=np.zeros((k_h,k_w),np.uint8)
        #slicing the img ac to kernel
        ver_s=i-1
        ver_e=k_h +ver_s
        hor_s=j-1
        hor_e= k_w+hor_s
        a=padded[ver_s:ver_e, hor_s:hor_e]
        #flatten a
        a=a.flatten()
        a.sort()
        median[i-1,j-1]=a[4]

plt.figure(figsize=(20,20))
'''
plt.subplot(121)
plt.imshow(img,cmap='gray')
plt.title('Original',fontsize=40)
plt.xticks([])
plt.yticks([])
plt.subplot(122)
plt.imshow(median,cmap='gray')
plt.title('filtered',fontsize=40)
plt.xticks([])
plt.yticks([])
plt.show()
'''

cv2_imshow(img)
cv2_imshow(median)
cv2.waitkey(0)