#erosion dilation
import numpy as np
import cv2


#req = urllib.request.urlopen('https://docs.opencv.org/master/binary.png')
#arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#img = cv2.imdecode(arr, 0)

#img=  cv2.imread('../lena_gray_256.tif',0)
img=  cv2.imread('/content/drive/My Drive/standard_test_images/cameraman.tif',0)

height,width = img.shape
img_flat=img.flatten()
sz=len(img_flat)
#print(sz)


#for otsu thresholding
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
            binary[i,j]=1 #cv2.imshow()does not supported ,to print change '1' to '255'
#cv2.imshow('binary',otsu)
#cv2.waitKey(0)




#structuring element
se=[[0,1,0],[1,1,1],[0,1,0]]
se1=[[1,0,1],[0,0,0],[1,0,1]]
s_h,s_w=3,3

se1 = np.array(se1, dtype=np.uint8)
se = np.array(se,dtype=np.uint8)
#print(se)

kernelcross = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))


#padded otsu
padded_otsu = np.pad(otsu,((1,1),(1,1)),'constant')
#padded binary
padded_binary = np.pad(binary,((1,1),(1,1)),'constant')

#print(padded_otsu)

erode = np.zeros((height,width),np.uint8)
dilate = np.zeros((height,width),np.uint8)

for i in range(1,height+1):
    for j in range(1,width+1):
        #slicing the img ac to kernel
        ver_s=i-1
        ver_e=s_h +ver_s
        hor_s=j-1
        hor_e= s_w+hor_s
        a=padded_otsu[ver_s:ver_e, hor_s:hor_e]
        #b=padded_binary[ver_s:ver_e, hor_s:hor_e]
        
        res= np.sum(np.multiply(a,se))
        #res= np.sum(np.multiply(b,se))

        
        if res == 5:
            erode[i-1,j-1]=1
        if res<5:
            erode[i-1,j-1]=0
        if res>=1:
            dilate[i-1,j-1]=1
        if res<1:
            dilate[i-1,j-1]=0


plt.figure(figsize=(15,15))
plt.subplot(131)
plt.imshow(erode,cmap='gray')
plt.title('erode',fontsize= 40)
plt.axis('off')

plt.subplot(132)
plt.imshow(dilate,cmap='gray')
plt.title('dilate',fontsize= 40)
plt.axis('off')

plt.subplot(133)
#plt.imshow(binary,cmap='gray')
#plt.title('binary',fontsize= 40)
plt.imshow(otsu,cmap='gray')
plt.title('otsu',fontsize=40)
plt.axis('off')
"""
plt.imshow(erode,cmap='gray')
plt.title('erode',fontsize= 40)

plt.imshow(dilate,cmap='gray')
plt.title('dilate',fontsize= 40)
"""
#req = urllib.request.urlopen('https://docs.opencv.org/master/binary.png')
#arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#image = cv2.imdecode(arr, 0)

#image=  cv2.imread('../lena_gray_256.tif')
image=  cv2.imread('/content/drive/My Drive/standard_test_images/cameraman.tif')

#_,thres=cv2.threshold(image,127,255,cv2.THRESH_BINARY)
_,thres=cv2.threshold(img,0,255,cv2.THRESH_OTSU)
imero = cv2.erode(thres,kernel =kernelcross,iterations = 1)
imdil = cv2.dilate(thres,kernel = kernelcross,iterations = 1)

plt.figure(figsize=(15,15))
plt.subplot(121)
plt.imshow(imero,cmap='gray')
plt.title('erode_cv2',fontsize= 40)
plt.axis('off')

plt.subplot(122)
plt.imshow(imdil,cmap='gray')
plt.title('dilate_cv2',fontsize= 40)
plt.axis('off')
plt.show()
#cv2.waitKey(0)