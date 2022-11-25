#hole filling
img=  cv2.imread('/content/drive/MyDrive/standard_test_images/convex.png',0)
#desired point to start
midi,midj = img.shape[0]//2,img.shape[1]//2
#print(img[i,j])
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
se=np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8)
se1=[[1,0,1],[0,0,0],[1,0,1]]
s_h,s_w=3,3

se1 = np.array(se1, dtype=np.uint8)
#se = np.array(se,dtype=np.uint8)

#padded otsu and binary
padded_otsu = np.pad(otsu,((1,1),(1,1)),'constant')
padded_binary = np.pad(binary,((1,1),(1,1)),'constant')


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
x =np.zeros_like(otsu,np.uint8)
xnew = x
x[midi,midj]=1
otsu_com = cv2.bitwise_not(otsu)
while True :
#for i in range(50):
  x= xnew
  padded_x = np.pad(x,((1,1),(1,1)),'constant')
  _,temp = erosion_dilation(padded_x,se)
  xnew = cv2.bitwise_and(temp,otsu_com)

  if(xnew==x).all():
    break
final = cv2.bitwise_or(xnew,otsu)
plt.imshow(final,'gray')
plt.axis('off')
plt.title('final image')
plt.show()

plt.imshow(img,'gray')
plt.axis('off')
plt.title('original image')
plt.show()
#erode,dilate= erosion_dilation(padded_otsu,se)