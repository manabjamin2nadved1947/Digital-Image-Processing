#wu tsai
import cv2
import math
img=  cv2.imread('/content/drive/My Drive/standard_test_images/cameraman.tif',0)
real_img = img.flatten()
height,width =img.shape
img_flat=img.flatten() #this will change

d = np.zeros((height*width),np.uint8)
#print(d)
img_flat = img_flat.astype('int16')
for i in range(0,img_flat.size-1):
    d[i] = abs(img_flat[i] - img_flat[i+1])
#print(d.size)

#stego_img
stego_img = cv2.imread('/content/drive/My Drive/standard_test_images/lena_gray_256.tif',0)
stego_height, stego_width = stego_img.shape
stego_flat = stego_img.flatten()

stego_flat_bin=''
"""
for i in range(stego_flat.size):
    t = bin(stego_flat[i])
    stego_flat_bin +=str(t[2:])
stego_flat_bin = bin(int(stego_flat_bin,2))[2:]
print("stego_flat_bin "+ f'{len(str(stego_flat_bin))}')
"""

for i in range(stego_flat.size):
    stego_flat_bin+=format(stego_flat[i],'08b')
stego_flat_bin+='0000000000'
#print("msg is "+f'{len(msg)}')   
#print(stego_flat_bin)



#encrytion
j=0 #indicate the  pointer pos in stega_flat_bin 
while i<d.size and j<len(stego_flat_bin):
    count =0
    code=''
    #difference table
    if d[i] >=0 and d[i]<=7:
        count=3 #3bit
        code= str(int(stego_flat_bin[j:j+3],2))
        j+=3
        lb = 0
    if d[i] >=8 and d[i]<=15:
        count =3 #3bit
        code= str(int(stego_flat_bin[j:j+3],2))
        j+=3
        lb=8
    if d[i] >=16 and d[i]<=31:
        count =4 #4bit
        code= str(int(stego_flat_bin[j:j+4],2))
        j+=4
        lb=16
    if d[i] >=32 and d[i]<=63:
        count =5 #5bit
        code= str(int(stego_flat_bin[j:j+5],2))
        j+=5
        lb=32
    if d[i] >=64 and d[i]<=127:
        count= 6 #take 6 bit
        code= str(int(stego_flat_bin[j:j+6],2))
        j+=6
        lb=64
    if d[i] >=128 and d[i]<=255:
        count = 7 #take 7 bit
        code= str(int(stego_flat_bin[j:j+7],2))
        j+=7
        lb=128
    #print(code)
    #j=0    
    """""
    while j<=len(stego_flat_bin):         
        for k in range(0,count):
            if j+k<=len(stego_flat_bin):
                code+=str(stego_flat_bin[j+k])
        break
    j+=k+1
    print(code)
    if code !='':
        code_dec = int(code,2)
    """""
    d_dash = lb+int(code)
    m= abs(d_dash - d[i])
    if (img_flat[i] >= img_flat[i+1]) and (d_dash >d[i]):
        img_flat[i] +=  math.ceil(m/2)
        img_flat[i+1] -= math.floor(m/2)
    
    if (img_flat[i] < img_flat[i+1]) and (d_dash > d[i]):
        img_flat[i] -=  math.floor(m/2)
        img_flat[i+1] += math.ceil(m/2)
    
    if (img_flat[i] >= img_flat[i+1]) and (d_dash <= d[i]):
        img_flat[i] -=  math.ceil(m/2)
        img_flat[i+1] += math.floor(m/2)
    
    if (img_flat[i] < img_flat[i+1]) and (d_dash <= d[i]):
        img_flat[i] +=  math.ceil(m/2)
        img_flat[i+1] -= math.floor(m/2)
    i+=1
img_flat = img_flat.astype('uint8')   
enc_img = np.zeros((height,width),np.uint8)
enc_img = np.reshape(img_flat,(height,width))


enc_img_flat = enc_img.flatten()
dd = np.zeros((height*width),np.uint8)

enc_img_flat = enc_img_flat.astype('int16')
for i in range(0,enc_img_flat.size-1):
    dd[i] = abs(enc_img_flat[i] - enc_img_flat[i+1]) #as img_flat modified it is now an encrypted image

i=0
count=0 #indicate the  pointer pos in stega_flat_bin
decode='' 
while i<dd.size and count<len(stego_flat_bin):
    #count =0
    
    #difference table
    if dd[i] >=0 and dd[i]<=7:
         #3bit
        lb = 0
        t = dd[i]-lb
        decode+= format(t,'03b')
        count+=3
        
    if dd[i] >=8 and dd[i]<=15:
         #3bit
        lb=8
        t = dd[i]-lb
        decode+= format(t,'03b')
        count+=3
        
    if dd[i] >=16 and dd[i]<=31:
         #4bit
        lb=16
        t = dd[i]-lb
        decode+= format(t,'04b')
        count+=4
        
    if dd[i] >=32 and dd[i]<=63:
         #5bit
        lb=32
        t = dd[i]-lb
        decode+= format(t,'05b')
        count+=5
        
    if dd[i] >=64 and dd[i]<=127:
         #take 6 bit
        lb=64
        t = dd[i]-lb
        decode+= format(t,'06b')
        count+=6
        
    if dd[i] >=128 and dd[i]<=255:
         #take 7 bit
        lb=128
        t = dd[i]-lb
        decode+= format(t,'07b')
        count+=7
    i+=1  

#print(decode)
dec_img = np.zeros((stego_height,stego_width),np.uint8)
#print(dec_img)
k=0
for i in range(stego_height):
    for j in range(stego_width):
        dec_img[i,j] = int(decode[k:k+8],2)
        k+=8

#staganalysis
mse=0
real_img = real_img.astype('int16')
enc_img_flat = img_flat.astype('int16')

for i in range(height*width):
    mse += (real_img[i]-enc_img_flat[i])**2
mse/=(height*width)
print("the mse is :"+ f'{mse}')

psnr = 20* math.log10(255/math.sqrt(mse))
print("the psnr is :"+ f'{psnr}')


plt.imshow(enc_img,'gray')
plt.title("encrypted image",color = "white" )
plt.show()
#plt.imshow(dec_img,'gray')
#plt.show()
#cv2.waitKey(0)
#cv2.imshow('enc_img',enc_img)
#cv2.waitKey(0)