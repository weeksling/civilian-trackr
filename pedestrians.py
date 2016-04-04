import cv2


class PedestrianTracker:
	def __init__ (self):
		self.unique_pedestrians = []
		self.last_frame
		self.setup_flag = False

	def initialize (self, found_contours, frame):
		self.unique_pedestrians = []
		self.last_frame = frame
		for cnt in found_contours:
			p = Pedestrian(cnt[0],cnt[1])
			self.unique_pedestrians.append(p)
		self.setup_flag=True

	def check_pedestrians (self, found_contours, current_frame)
		if (self.setup_flag == False):
			self.initialize(found_contours, current_frame)
		else:
			p1, st, err = cv2.calcOpticalFlowPyrLK(self.last_frame, current_frame)
			print p1