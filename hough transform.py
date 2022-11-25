#hough transform
img=  cv2.imread('/content/drive/MyDrive/standard_test_images/cameraman.tif',0)
img=  cv2.imread('/content/drive/MyDrive/standard_test_images/soduku.png',0)
#img=  cv2.imread('/content/drive/MyDrive/standard_test_images/connected.png',0)


width,height = img.shape
img_diagonal = round(np.sqrt((width**2)+ (height**2)))

canny = cv2.Canny(img,50,200)
#cv2_imshow(canny)
theta = np.deg2rad(np.arange(-90.0, 91.0,step=1))
rohs = np.arange(-img_diagonal, img_diagonal+1, step=1)
#rohs = np.linspace(-img_diagonal, img_diagonal, 2*img_diagonal)

#print(theta)
#print(rohs)
cos = np.cos(theta)
sin = np.sin(theta)
#print(f'cos = {cos} \nsin = {sin}')
#print(img_diagonal)

accumulator = np.zeros((2*img_diagonal, len(theta)),np.uint8)

#get (y-axis,x-axis) for white(foreground) points only
b = np.argwhere(canny==255)
#print(b)

coordinates = list(zip(b[0],b[1]))
#print(coordinates)  #coordinates[0] = y-axis coordinates[1]= x-axis
#print(accumulator.shape)
#print(coordinates[3][1])
"""
for c in range (len(coordinates)):
  x = coordinates[c][1]
  y = coordinates[c][0]
"""
for i in range (len(b)):
  x = b[i][1]
  y = b[i][0] 
  for t in range(len(theta)):
    rho = int(round(x*cos[t]+y*sin[t]))
    accumulator[rho,t]+=1
#cv2_imshow(accumulator)
#print(np.amax(accumulator))
thres_array = np.argwhere(accumulator>=200)
#print(len(thres_array))
img_copy = img.copy()

cv2_imshow(accumulator)
print(accumulator)