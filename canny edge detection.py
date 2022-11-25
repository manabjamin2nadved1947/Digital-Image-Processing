#canny edge detection
import cv2
import numpy as np

img = cv2.imread('/content/drive/My Drive/standard_test_images/peppers_gray.tif',0)
img = cv2.GaussianBlur(img, (3, 3), 0)
height,width = img.shape
padded = np.pad(img,((1,1),(1,1)),'constant')
k_h,k_w=3,3

gx = np.zeros((height,width))
gy =np.zeros((height,width))
m= np.zeros((height,width))
alpha=np.zeros((height,width))

kernel_sx = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
kernel_sy = kernel_sx.T

for i in range(1,height+1):
    for j in range(1,width+1):
        #slicing the img ac to kernel
        ver_s=i-1
        ver_e=k_h +ver_s
        hor_s=j-1
        hor_e= k_w+hor_s
        a=padded[ver_s:ver_e, hor_s:hor_e]
        #blur[i-1,j-1]= np.sum(np.multiply(a,kernel_gauss))
        gy[i-1,j-1]=np.sum(np.multiply(a,kernel_sy))
        gx[i-1,j-1]=np.sum(np.multiply(a,kernel_sx))
for i in range(height):
    for j in range(width):
        m[i,j] = np.sqrt(np.square(gy[i,j])+np.square(gx[i,j]))
        alpha[i,j]=np.rad2deg(np.arctan2(gy[i,j],gx[i,j]))
alpha[alpha<0]+=180
m_padded = np.pad(m,((1,1),(1,1)),'constant')
alpha_padded = np.pad(alpha,((1,1),(1,1)),'constant')
gn = np.zeros((height,width))
#d=np.zeros((height,width))      

 #non-max suppression
for i in range(1,height+1):
    for j in range(1,width+1):
        #slicing the img ac to kernel
        ver_s=i-1
        ver_e=k_h +ver_s
        hor_s=j-1
        hor_e= k_w+hor_s
        a=m_padded[ver_s:ver_e, hor_s:hor_e]
        b=alpha_padded[ver_s:ver_e, hor_s:hor_e]
        if(0 <=b[1,1]<22.5) or (157.5<=b[1,1]<=180):
            if a[1,1] >= max(a[1,0],a[1,2]):
                gn[i-1,j-1]=a[1,1]

        elif(22.5<b[1,1]<=67.5):
            if a[1,1] >= max(a[0,0],a[2,2]):
                gn[i-1,j-1] = a[1,1]
        elif(67.5<b[1,1]<=112.5):
            if a[1,1] >= max(a[0,1],a[2,1]):
                gn[i-1,j-1] = a[1,1]
        else: 
            if a[1,1] >= max(a[2,0],a[0,2]):
                gn[i-1,j-1] = a[1,1]
gn = gn.astype('uint8')
#m = m.astype('uint8')
#print(gn)

#hyteresis thresholding
low_thres= 50
high_thres = 200
glow = np.zeros(img.shape) 
ghigh = np.zeros(img.shape) #strong edge
"""
for i in range(height):
    for j in range(width):
        if(gn[i,j]>=high_thres):
            ghigh[i,j]=gn[i,j]
        #elif(gn[i,j]<high_thres):
         #   ghigh[i,j]=0
        elif(gn[i,j]>=low_thres):
            glow[i,j]=gn[i,j]
        #elif(gn[i,j]<=low_thres):
         #   glow[i,j]=0
count=0
for i in range(height):
    for j in range(width):
        glow[i,j] = glow[i,j]-ghigh[i,j]
        if(glow[i,j]<0):
            count+=1 


plt.imshow(ghigh,cmap='gray')
plt.axis('off')
plt.show()
"""
out = np.zeros(gn.shape,np.uint8)

strong_i,strong_j = np.where(gn>=high_thres)
zeros_i,zeros_j = np.where(gn<low_thres)

weak_i,weak_j = np.where((gn<high_thres) & (gn>=low_thres))

out[strong_i,strong_j] = 255
out[zeros_i,zeros_j] = 0
out[weak_i,weak_j] =80

for i in range(1,out.shape[0]-1):
    for j in range(1,out.shape[1]-1):
        if(out[i,j]==75):
            if 255 in [out[i+1,j-1],out[i+1,j],out[i+1,j+1],out[i,j-1],out[i,j+1],out[i-1,j-1],out[i-1,j],out[i-1,j+1]]:
                out[i,j]=255
            else:
                out[i,j]=0

plt.figure(figsize=(7,7))
plt.imshow(out,'gray')
plt.axis('off')
plt.show()
