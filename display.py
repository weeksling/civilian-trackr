import cv2

class Overlay:
  def __init__(self, frame):
    self.frame = frame
    self.total_count = 0
    self.on_screen_count = 0

  def set_total_count(self, total):
    self.total_count = total

  def increment_screen_count(self):
    self.on_screen_count += 1

  def display(self):
    overlay = self.frame.copy()
    cv2.rectangle(overlay, (420,320),(650,370),(128,128,128), -1)
    alpha = 0.8
    cv2.addWeighted(overlay, alpha, self.frame, 1 - alpha, 0, self.frame)
    cv2.putText(self.frame, "Pedestrian Count (Total): {}".format(str(self.total_count)), (425, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,0,0), 1)
    cv2.putText(self.frame, "Pedestrian Count (On Screen): {}".format(str(self.on_screen_count)), (425, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,0,0), 1)