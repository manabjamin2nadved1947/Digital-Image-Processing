#blurring
import cv2 
import numpy as np
import matplotlib.pyplot as plt

img=cv2.imread('/content/drive/My Drive/standard_test_images/lena_gray_256.tif',0)
padded = np.pad(img,((1,1),(1,1)),'constant')
height,width = img.shape

kernel_blur= np.ones((3,3),np.uint8)/9
kernel_gauss = np.array([[1,4,1],[4,8,4],[1,4,1]])/28
k_h,k_w=kernel_blur.shape

blur_gauss=np.zeros((height,width),np.uint8)
blur=np.zeros((height,width),np.uint8)

for i in range(1,height+1):
    for j in range(1,width+1):
        ver_s=i-1
        ver_e=k_h +ver_s
        hor_s=j-1
        hor_e= k_w+hor_s
        a=padded[ver_s:ver_e, hor_s:hor_e]
        blur_gauss[i-1,j-1]= np.sum(np.multiply(a,kernel_gauss))
        blur[i-1,j-1]= np.sum(np.multiply(a,kernel_blur))


plt.figure(figsize=(45,45))

plt.subplot(131)
plt.imshow(img,cmap='gray')
plt.title('Original',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.subplot(132)
plt.imshow(blur,cmap='gray')
plt.title('blur(average)',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.subplot(133)
plt.imshow(blur_gauss,cmap='gray')
plt.title('blur(gaussian)',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.show()