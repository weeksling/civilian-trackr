import argparse
import tracker
import cv2

if __name__ == '__main__':
  ap = argparse.ArgumentParser()
  ap.add_argument("-v", "--video", help="video file")
  args = vars(ap.parse_args())
 
  if args["video"] is not None:
    camera = cv2.VideoCapture(args["video"])
    tracker.track(camera)
  else:
    print "USAGE: python run_trackr --video <VIDEO_FILE>"
    ap.exit()
