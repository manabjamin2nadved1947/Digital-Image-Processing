#opening closing
import numpy as np
import cv2

#img=  cv2.imread('../lena_gray_256.tif',0)
img=  cv2.imread("/content/drive/My Drive/standard_test_images/mandril_gray.tif", 0)
#img=  cv2.imread("/content/drive/My Drive/standard_test_images/convex.png", 0)
height,width = img.shape
img_flat=img.flatten()
sz=len(img_flat)
#print(sz)



#binary thresholding
binary = np.zeros((height,width),np.uint8)

for i in range(height):
    for j in range(width):
        if(img[i,j]<127):
            binary[i,j]=0
        else:
            binary[i,j]=1 #cv2.imshow()does not supported ,to print change 1 to 255

#structuring element
se=[[0,1,0],[1,1,1],[0,1,0]]
se1=[[1,0,1],[0,0,0],[1,0,1]]
s_h,s_w=3,3

se1 = np.array(se1, dtype=np.uint8)
se = np.array(se,dtype=np.uint8)
#print(se)

#padded otsu

padded_binary = np.pad(binary,((1,1),(1,1)),'constant')
#print(padded_otsu)

def erosion_dilation(img,se):
    #height,width = img.shape
    erode = np.ones((height,width),np.uint8)
    dilate = np.zeros((height,width),np.uint8)
    s_h,s_w=3,3
    for i in range(1,height+1):
        for j in range(1,width+1):
            #slicing the img ac to kernel
            ver_s=i-1
            ver_e=s_h +ver_s
            hor_s=j-1
            hor_e= s_w+hor_s
            #a=padded_otsu[ver_s:ver_e, hor_s:hor_e]
            b=img[ver_s:ver_e, hor_s:hor_e]
            #print(b)
            #res= np.sum(np.multiply(a,se))
            
            res= np.sum(np.multiply(b,se))

        
            for k in range(3):
              for l in range(3):
                if(b[k,l]==0 and se[k,l]==1):
                  erode[i-1,j-1]=0
                  break
                
            if res>=1: 
              dilate[i-1,j-1]=1
            if(res<1):
              dilate[i-1,j-1]=0
            
    return (erode,dilate)
erode = np.zeros((height,width),np.uint8)
dilate = np.zeros((height,width),np.uint8)
erode,dilate = erosion_dilation(padded_binary,se)

#opening=np.zeros((height,width),np.uint8)
#closing=np.zeros((height,width),np.uint8)
padded_erode = np.pad(erode,((1,1),(1,1)),'constant')
padded_dilate = np.pad(dilate,((1,1),(1,1)),'constant')
_,opening = erosion_dilation(padded_erode,se) #erosion followed by dilation
closing,_ = erosion_dilation(padded_dilate,se) #dilation followed by erosion

plt.figure(figsize=(10,10))
plt.subplot(121)
plt.imshow(opening,cmap='gray')
plt.title('opening',fontsize= 40)
plt.axis('off')

plt.subplot(122)
plt.imshow(closing,cmap='gray')
plt.title('closing',fontsize= 40)
plt.axis('off')
plt.show()