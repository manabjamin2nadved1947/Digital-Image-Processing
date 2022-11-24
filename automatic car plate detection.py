# automatic car plate detection using opencv

import cv2
import imutils #to resize image
import pytesseract
import urllib.request
pytesseract.pytesseract.tesseract_cmd = (r"/usr/bin/tesseract")

req = urllib.request.urlopen('https://gomechanic.in/blog/wp-content/uploads/2019/05/typesofcarnumberplates-02-01.jpg')
#req = urllib.request.urlopen('https://i.guim.co.uk/img/media/7abd54075e036e3843ec6e82793dca29e6430db0/478_663_2586_1552/master/2586.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=4ee9c128a408ec7192b649c3593574c4')
#req = urllib.request.urlopen('https://cdn.skoda-storyboard.com/2019/02/GB-number-plate-2-header-V3-1920x730.jpg')
#req = urllib.request.urlopen('https://imgk.timesnownews.com/story/car_with_covid_19_number_plate.jpg?tr=w-1200,h-900')
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, 0)

img = imutils.resize(img,width=500)
#img2  = cv2.bilateralFilter(img, 11,17,17)
img2 = cv2.GaussianBlur(img,(5,5),1)
#canny_img = cv2.Canny(img2, 50, 100)
canny_img = cv2.Canny(img2, 170, 200)
#find contours
contours, hirearchy = cv2.findContours(canny_img.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
canny_copy = canny_img.copy()
cv2.drawContours(canny_copy, contours, -1, (100,100,200),5)
cv2_imshow(canny_copy)
print("contours")
#sort the contours list in desc order and take 30 largest countours out of it
contours = sorted(contours , key = cv2.contourArea, reverse=True)[:30]
img_conts = img2.copy()
cv2.drawContours(img_conts,contours,-1,(100,100,200),5)
cv2_imshow(img_conts)
print("desired region's contour")
Numberplatecount = None
count = 0 
name = 1 #name of the cropped image

for i in contours:
  perimeter = cv2.arcLength(i, True)
  approx = cv2.approxPolyDP(i, .02*perimeter, True)
  if len(approx)==4:
    Numberplatecount = approx
    x,y,width,height = cv2.boundingRect(i)
    crp_img = img[y:y+height, x:x+width]
    cv2.imwrite(str(name)+'.png', crp_img)
    name+=1
    break
cv2.drawContours(img2,[Numberplatecount],-1,(0, 230, 255),6)
cv2_imshow(img2)
print("detected car plate in border")
crop_img_loc = '1.png'
cv2_imshow(cv2.imread(crop_img_loc))
print("cropped detected car plate")
#print(pytesseract.image_to_string(crop_img_loc))


plt.figure(figsize=(15,15))
plt.subplot(131)
plt.imshow(img,cmap= 'gray')
plt.title('original image')
plt.axis('Off')
plt.subplot(132)
plt.imshow(img2,cmap= 'gray')
plt.title('processed image')
plt.axis('Off')
plt.subplot(133)
plt.imshow(canny_img,cmap= 'gray')
plt.title('canny edge detection')
plt.axis('Off')
plt.show()

