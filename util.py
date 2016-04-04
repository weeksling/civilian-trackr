import cv2

def overlay(frame, contours):
  # apply overlay to frame
  overlay = frame.copy()
  cv2.rectangle(overlay, (420,320),(650,370),(128,128,128), -1)
  alpha = 0.8
  cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
  cv2.putText(frame, "Pedestrian Count (Total): {}".format("undefined"), (425, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,0,0), 1)
  cv2.putText(frame, "Pedestrian Count (On Screen): {}".format(str(len(contours))), (425, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,0,0), 1)