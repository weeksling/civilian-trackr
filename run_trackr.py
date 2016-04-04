import argparse
import tracker
import cv2

if __name__ == '__main__':
  ap = argparse.ArgumentParser()
  ap.add_argument("-v", "--video", help="path to the video file")
  args = vars(ap.parse_args())
 
  camera = cv2.VideoCapture(args["video"])

  tracker.track(camera)
