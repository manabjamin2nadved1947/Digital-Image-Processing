#laplacian edge detection
img=cv2.imread('/content/drive/My Drive/standard_test_images/house.tif',0)
height,width =  img.shape
padded= np.pad(img,((1,1),(1,1)),'constant')

k_h,k_w=3,3
kernel=np.array([[0,1,0],[1,-4,1],[0,1,0]])

laplacian = np.zeros((height,width),np.uint8)


for i in range(1,height+1):
    for j in range(1,width+1):
        #slicing the img ac to kernel
        ver_s=i-1
        ver_e=k_h +ver_s
        hor_s=j-1
        hor_e= k_w+hor_s
        a=padded[ver_s:ver_e, hor_s:hor_e]
        #laplacian operation
        laplacian[i-1,j-1]=np.sum(np.multiply(a,kernel))
        


plt.figure(figsize=(30,30))

plt.subplot(121)
plt.imshow(img,cmap='gray')
plt.title('Original',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.subplot(122)
plt.imshow(laplacian,cmap='gray')
plt.title('laplacian',fontsize=60)
plt.xticks([])
plt.yticks([])
plt.show()