import cv2
import numpy as np
import argparse

def track(cam):

  for_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7, 7))  
  for_di = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15, 20))

  f, img = cam.read()
  background = np.float32(img)

  while(cam.isOpened): 
    f,img=cam.read()
    
    if f==True:

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
    
      my_blobs = []
      for cnt in contours:
        try:
          x,y,w,h = cv2.boundingRect(cnt)
          
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

if __name__ == '__main__':
  ap = argparse.ArgumentParser()
  ap.add_argument("-v", "--video", help="path to the video file")
  args = vars(ap.parse_args())

  camera = None

  # if the video argument is None, then we are reading from webcam
  if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
   
  # otherwise, we are reading from a video file
  else:
    camera = cv2.VideoCapture(args["video"])

  track(camera)

