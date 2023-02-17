import cv2

# Read the input image
img = cv2.imread('./pictures/stellina.jpg')

# convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding in the gray image to create a binary image
ret,thresh = cv2.threshold(gray,150,255,0)

# Find the contours using binary image
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print("Number of contours in image:",len(contours))
for cnt in contours:
    #cnt = contours[i]
    # compute the area and perimeter
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    perimeter = round(perimeter, 4)

    if(area > 1000):
        print('Area:', area)
        print('Perimeter:', perimeter)
        img1 = cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
        x1, y1 = cnt[0,0]


cv2.imshow("Image", img)    
cv2.waitKey(0)
cv2.destroyAllWindows()