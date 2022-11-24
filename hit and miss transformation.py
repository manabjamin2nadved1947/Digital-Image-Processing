#hit and miss
import numpy as np
import cv2

img=  cv2.imread('../lena_gray_256.tif',0)
img=  cv2.imread('../cameraman.tif',0)
img=cv2.imread("/content/drive/My Drive/standard_test_images/woman_blonde.tif", 0)
#img=cv2.imread('../house.tif',0)

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
#cv2.imshow('binary',otsu)
#cv2.waitKey(0)

#structuring element
se1=np.array([[-1,1,-1],[0,1,1],[0,0,-1]])
se2=np.array([[-1,1,-1],[1,1,0],[-1,0,0]])
se3=np.array([[-1,0,0],[1,1,0],[-1,1,-1]])
se4=np.array([[0,0,-1],[0,1,1],[-1,1,-1]])

s_h,s_w=3,3
#print(se)

#padded otsu
padded_otsu = np.pad(otsu,((1,1),(1,1)),'constant')
padded_binary = np.pad(binary,((1,1),(1,1)),'constant')
#print(padded_otsu)


def hit_and_miss1(img,se):
    #print(se)
    b = np.ones((height,width),np.uint8)
    for i in range(1,height+1):
        for j in range(1,width+1):
            #slicing the img ac to kernel
            ver_s=i-1
            ver_e=s_h +ver_s
            hor_s=j-1
            hor_e= s_w+hor_s
            a=img[ver_s:ver_e, hor_s:hor_e]
            #bina=padded_binary[ver_s:ver_e, hor_s:hor_e]
            #b[i,j]=1
            for m in range(3):
                for n in range(3):
                    if(se[m,n]!=a[m,n] and se[m,n]!=-1):
                        b[i-1,j-1]=0
                        break
    #print(b)
    return b
def hit_miss2(im,*args): #input padded image output: non-padded
    h_m = np.zeros((height,width),np.uint8)
    for i in args:

      b= hit_and_miss1(im,i)
      #print(b.shape)
      #print(h_m.shape)
      h_m = cv2.bitwise_or(h_m,b)

    
    return h_m
h_m = hit_miss2(padded_otsu, se1,se2,se3,se4)


plt.imshow(h_m,'gray')
plt.title('hit and miss', color='black')
plt.axis('off')
plt.show()

plt.imshow(otsu,'gray')
plt.title('input binary(otsu) image', color='white')
plt.axis('off')
plt.show()