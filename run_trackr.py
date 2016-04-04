import argparse
import tracker
import cv2

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

  tracker.track(camera)
