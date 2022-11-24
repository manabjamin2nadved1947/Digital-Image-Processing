#sobel edge detection
img=cv2.imread('/content/drive/My Drive/standard_test_images/house.tif',0)
height,width =  img.shape
padded= np.pad(img,((1,1),(1,1)),'constant')

k_h,k_w=3,3 #kernel shape

kernel_sy=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
kernel_sx=kernel_sy.T

sobely = np.zeros((height,width),np.uint8)
sobelx = np.zeros((height,width),np.uint8)
sobel_res= np.zeros((height,width),np.uint8)

for i in range(1,height+1):
    for j in range(1,width+1):
        #slicing the img ac to kernel
        ver_s=i-1
        ver_e=k_h +ver_s
        hor_s=j-1
        hor_e= k_w+hor_s
        a=padded[ver_s:ver_e, hor_s:hor_e]
        #sobel operation
        sobely[i-1,j-1]=np.sum(np.multiply(a,kernel_sy))
        sobelx[i-1,j-1]=np.sum(np.multiply(a,kernel_sx))


for i in range(height):
    for j in range(width):
        sobel_res[i,j]= np.sqrt((sobelx[i,j]**2)+(sobely[i,j]**2))

plt.figure(figsize=(30,30))

plt.subplot(221)
plt.imshow(img,cmap='gray')
plt.title('Original',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.subplot(222)
plt.imshow(sobelx,cmap='gray')
plt.title('sobelx',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.subplot(223)
plt.imshow(sobely,cmap='gray')
plt.title('sobely',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.subplot(224)
plt.imshow(sobel_res,cmap='gray')
plt.title('sobel_res',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.show()