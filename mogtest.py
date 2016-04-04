import cv2
import numpy as np

cam=cv2.VideoCapture('demo.avi')
# fgbg = cv2.BackgroundSubtractorMOG()

for_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7, 7))  
for_di = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15, 20))

f, img = cam.read()
background = np.float32(img)

while(cam.isOpened): 
  f,img=cam.read()
  
  if f==True:

    # img=cv2.medianBlur(img,3)
    # grey_image = fgbg.apply(img)
    cv2.accumulateWeighted(img, background, 0.01)
    im_zero = cv2.convertScaleAbs(background)
    # im_zero = background.astype(np.uint8)

    cv2.imshow("Im_zero", im_zero)

    #  Get the first diff image - this is raw motion 
    d1 = cv2.absdiff(img, im_zero)

    #  Convert this to greyscale
    gray_image = cv2.cvtColor(d1, cv2.COLOR_BGR2GRAY)

    thresh, im_bw = cv2.threshold(gray_image, 15, 255, cv2.THRESH_BINARY)
    im_er = cv2.erode(gray_image, for_er)
    im_dl = cv2.dilate(im_er, for_di)


    contours, hierarchy = cv2.findContours(im_dl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
    my_blobs = []
    for cnt in contours:
      try:
        x,y,w,h = cv2.boundingRect(cnt)
        
        #print "Rect: " , w , " " , h
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        
        moments = cv2.moments(cnt)
        x = int(moments['m10'] / moments['m00'])
      except:
        print "Bad Rect"

    cv2.imshow('thresholded frames',im_bw)
    cv2.imshow('video', img)
    cv2.imshow('erosion/dilation', im_dl)
  if(cv2.waitKey(27)!=-1):
    cam.release()
    cv2.destroyAllWindows()
    break 
cam.release()
cv2.destroyAllWindows()

