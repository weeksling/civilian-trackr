import cv2
import numpy as np

import display

snapshots = 0

def track(cam):

  for_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7, 7))  
  for_di = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15, 20))

  f, img = cam.read()
  background = np.float32(img)

  while(cam.isOpened): 
    f,img=cam.read()
    if f == True:
      img_original = img.copy()

      cv2.accumulateWeighted(img, background, 0.01)
      im_zero = cv2.convertScaleAbs(background)

      cv2.imshow("Im_zero", im_zero)

      #  Get the first diff image - this is raw motion 
      d1 = cv2.absdiff(img, im_zero)

      #  Convert this to greyscale
      gray_image = cv2.cvtColor(d1, cv2.COLOR_BGR2GRAY)

      thresh, im_bw = cv2.threshold(gray_image, 15, 255, cv2.THRESH_BINARY)
      im_er = cv2.erode(im_bw, for_er)
      im_dl = cv2.dilate(im_er, for_di)


      contours, hierarchy = cv2.findContours(im_dl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
      blobs = []
      for cnt in contours:
        try:
          x,y,w,h = cv2.boundingRect(cnt)
          
          cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
          
          moments = cv2.moments(cnt)
          x = int(moments['m10'] / moments['m00'])
          y = int(moments['m01'] / moments['m00'])
          blobs.append((x,y))
        except:
          print "Bad Rect"

      if len(blobs)>0:
        pedestrian_tracker.check_pedestrians(blobs, im_dl)
        
      display.overlay(img, contours)

      cv2.imshow('thresholded frames',im_bw)
      cv2.imshow('video', img)
      #cv2.imshow('erosion/dilation', im_dl)
    key_pressed = cv2.waitKey(27)
    if (key_pressed==32):
      capture(img_original, contours)
    elif (key_pressed==27):
      print key_pressed
      cam.release()
      cv2.destroyAllWindows()
      break 
  cam.release()
  cv2.destroyAllWindows()

def capture (frame, contours):
  global snapshots
  for cnt in contours:
    try:
      x,y,w,h = cv2.boundingRect(cnt)
      snapshots = snapshots + 1
      crop_img = frame[y:y+h,x:x+w]
      title = 'output/snapshot_' + `snapshots`+'.png'
      cv2.imwrite(title,crop_img)
    except:
      print 'Capture failed!'
      continue



