#Boundary Extraction
import numpy as np
import cv2

#img=  cv2.imread('../lena_gray_256.tif',0)
img=  cv2.imread('/content/drive/MyDrive/standard_test_images/house.tif',0)

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
            otsu[i,j]=1#cv2.imshow()does not supported ,to print change 1 to 255


#binary thresholding
binary = np.zeros((height,width),np.uint8)

for i in range(height):
    for j in range(width):
        if(img[i,j]<127):
            binary[i,j]=0
        else:
            binary[i,j]=1 #cv2.imshow()does not supported ,to print change 1 to 255

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
padded_otsu = np.pad(otsu,((1,1),(1,1)),'constant')
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

            """
            if res == 5:
                erode[i-1,j-1]=1
            if res<5:
                erode[i-1,j-1]=0
            if res>=1:
                dilate[i-1,j-1]=1
            if res<1:
                dilate[i-1,j-1]=0
            """
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
erode,dilate = erosion_dilation(padded_otsu,se)
boundary = np.zeros((height,width),np.uint8)
padded_erode = np.pad(erode,((1,1),(1,1)),'constant')
boundary = padded_otsu - padded_erode
plt.imshow(boundary,cmap='gray')
plt.title('boundary',fontsize= 40)
plt.axis('off')
plt.show()

plt.imshow(img,cmap='gray')
plt.title('original',fontsize= 40)
plt.axis('off')
plt.show()