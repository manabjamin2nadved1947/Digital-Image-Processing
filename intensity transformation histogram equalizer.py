#histogram equilizer
import numpy as np
import cv2

img=  cv2.imread('../low_contrast.png',0)
#img = cv2.resize(img,(256,256))
height,width = img.shape
img_flat=img.flatten()
#print(img_flat)

#create dictionary to calculate freq of each pixels
dict={}
for i in img_flat:
    if i in dict:
        dict[i]+=1
    else:
        dict[i]=1

#sorted = sorted(dict.items())
#print(sorted)

#create pdf for input pixels 
pdf =np.zeros((256))
for key in dict:
    #print(key)
    pdf[key] = dict[key]
#print(pdf[100])
#print(dict[100])

for i in range(256):
    pdf[i]/=len(img_flat)
#print(pdf[100])

#print(pdf)
#(cdf in) transformation function    
s= np.zeros((256))
s[0]=255*pdf[0]

for i in range(1,256):
    s[i]=s[i-1]+255*pdf[i]
    #print(s[i])
s_round = np.zeros((256),np.uint8)
s_round = np.around(s)
#print(s_round)


hist_eq= np.zeros((height,width),np.uint8)

for i in range(height):
    for j in range(width):
        hist_eq[i,j]= s_round[img[i,j]]
'''

eq = cv2.equalizeHist(img)
cv2.imshow('hist_eq',hist_eq)
cv2.imshow('eq',eq)
cv2.imshow('img',img)

cv2.waitKey(0)
'''

#plt.imshow(hist_eq,'gray')
#plt.show()

plt.figure(figsize=(45,45))
plt.subplot(121)
plt.imshow(img,cmap='gray')
plt.title('Original',fontsize= 40)
plt.axis('off')

plt.subplot(122)
plt.imshow(hist_eq,cmap='gray')
plt.title('hist_eq',fontsize= 40)
plt.axis('off')
plt.show()

plt.figure(figsize=(8,8))
bins = [i for i in range(256)]
label = ['Original','hist_eq']
arr = [img_flat,hist_eq.flatten()]
plt.hist(arr,bins=bins,label=label)
plt.title('hist',fontsize=20)
plt.xlabel('pix',fontsize=20)
plt.ylabel('freq',fontsize=20)
plt.legend(loc = 'upper right',fontsize=10)
plt.show()