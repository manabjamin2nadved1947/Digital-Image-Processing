#otsu thresholding
import numpy as np
import cv2

img=  cv2.imread('/content/drive/My Drive/standard_test_images/cameraman.tif',0)

height,width = img.shape
img_flat=img.flatten()
sz=len(img_flat)
#print(sz)

#create dictionary to calculate freq of each pixels
dict={}
for i in img_flat:
    if i in dict:
        dict[i]+=1
    else:
        dict[i]=1

freq =np.zeros((256))
for key in dict:
    #print(key)
    freq[key] = dict[key]

#between class variance
bet_class_var=np.zeros((256))
max_variance=0

for thres in range(256):
    #background
    sum_b=0
    w_b=0
    mean_b=0
    
    for b in range(thres):
        sum_b+= freq[b]

    for b in range(thres):
        w_b+=freq[b]/sz
        if(sum_b!=0):
            mean_b+= (b*freq[b])/sum_b
    #foreground
    sum_f=0
    w_f=0
    mean_f=0

    for f in range(thres,256):
        sum_f+=freq[f]
    for f in range(thres,256):
        w_f+=freq[f]/sz
        if(sum_f!=0):
            mean_f+=(f*freq[f])/sum_f

    bet_class_var[thres]= w_b * w_f * (mean_b - mean_f)**2

    if(bet_class_var[thres]>max_variance):
        max_variance = bet_class_var[thres]
        threshold=thres

#print(threshold)
otsu = np.zeros((height,width),np.uint8)

for i in range(height):
    for j in range(width):
        if(img[i,j]<threshold):
            otsu[i,j]=0
        else:
            otsu[i,j]=1

#print(otsu)
#cv2.imshow('otsu',otsu)
#cv2.waitKey(0)
plt.figure(figsize=(15,15))

plt.subplot(121)
plt.imshow(img,cmap='gray')
plt.title('Original',fontsize=40,color='white' )
plt.axis('off')

plt.subplot(122)
plt.imshow(otsu,cmap='gray')
plt.title('otsu',fontsize=40,color='white' )
plt.axis('off')

plt.show()