#lsb stego
import hashlib
import cv2
filename = '/content/drive/My Drive/standard_test_images/cameraman.tif' #input("enter the file name: ")

with open (filename,"rb") as f:
    bytes = f.read()
    readabale_hash = hashlib.sha256(bytes).hexdigest()
    print("the readabale_hash is: "+ readabale_hash)

decimal = int(readabale_hash,16)
#print("the decimal is "+ f'{dec}')

#global bin 
bin= bin.format(decimal)
#print(bin)

b=bin[2:]
#print(len(b))

#print("the hex code is " + f'{hex(int(b,2))}')

img=  cv2.imread('/content/drive/My Drive/standard_test_images/cameraman.tif',0)
real_img = img.flatten()
height,width =img.shape
img_flat=img.flatten()
string =b

#string = ''.join(format(x,'b') for x in bytearray(string, 'utf-8'))


#encrypt
for i in range(len(string)):
    if (img_flat[i] & 1) !=int(string[i]):
        if int(string[i])==0:
            img_flat[i]-=1
        elif int(string[i])==1:
            img_flat[i]+=1

stego = np.zeros((height,width),np.uint8)
stego = np.reshape(img_flat,(height,width))

#decrypt 
dec=""
stego_flat=stego.flatten()
for  i in range(256):
    dec = dec + str(stego_flat[i] & 1)
print("the decrypted msg is:  " + f'{hex(int(dec,2))[2:]}')

#res = int(b,2) - int(dec,2)
#print ("the diff between enc and dec msg  is : " + f'{res}')


#steganalysis
import math
mse=0
real_img = real_img.astype('int16')
stego_flat = stego_flat.astype('int16')

for i in range(height*width):
    mse += (real_img[i]-stego_flat[i])**2
mse/=(height*width)
print("the mse is :"+ f'{mse}')

psnr = 20* math.log10(255/math.sqrt(mse))
print("the psnr is :"+ f'{psnr}')

plt.figure(figsize=(5,5))
plt.imshow(stego,cmap='gray')
plt.title('Stego',fontsize=40,color='white' )
plt.axis('off')
plt.show()

plt.figure(figsize=(5,5))
plt.imshow(img,cmap='gray')
plt.title('Original',fontsize=40,color='white' )
plt.axis('off')
plt.show()    