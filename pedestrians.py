import cv2
import numpy as np
import math

pedestrian_id = 0
VOTES_REQ = 20
PEDESTRIAN_LIFE = 3
CANDIDATE_LIFE = 3
DIST_LIMIT = 20
def distance(p0, p1):
		return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

class Candidate:
	def __init__(self, x,y):
		global pedestrian_id
		self.x = x
		self.y = y
		self.votes = 1
		self.life = CANDIDATE_LIFE

	def update_location(self, x, y):
		self.x = x
		self.y = y
		self.votes = self.votes + 1
		self.life = CANDIDATE_LIFE

	def get_location(self):
		return (self.x, self.y)

class Pedestrian:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.life = PEDESTRIAN_LIFE
		self.is_alive = True
		self.was_updated = False

	def update_location (self, x, y):
		self.x = x
		self.y = y
		self.life = PEDESTRIAN_LIFE

	def get_location (self):
		return (self.x, self.y)

class PedestrianTracker:
	def __init__ (self):
		self.unique_pedestrians = []
		self.candidates = []
		self.setup_flag = False

	def initialize (self, found_contours, frame):
		self.candidates = []
		for cnt in found_contours:
			p = Pedestrian(cnt[0],cnt[1])
			self.unique_pedestrians.append(p)
		self.setup_flag=True

	def prune(self):
		for ped in self.unique_pedestrians:
			if ped.was_updated:
				ped.was_updated = False
			else:
				ped.life = ped.life - 1
				if ped.life<0:
					ped.is_alive = False

	def check_pedestrians (self, found_contours, current_frame):
		if (self.setup_flag == False):
			self.initialize(found_contours, current_frame)
		else:
			for found in found_contours:
				matched = False

				for known in self.unique_pedestrians:
					if known.is_alive:
						if (distance(found, known.get_location())<DIST_LIMIT) and known.is_alive:
							matched = True
							known.update_location(found[0], found[1])
							known.was_updated = True

				# If no matching pedestrians were found, search for an existing candidate
				if matched == False:
					for known in self.candidates:
						if distance(found, known.get_location())<DIST_LIMIT:
							matched = True
							known.update_location(found[0], found[1])
							# If the number of votes is met, promote candidate to pedestrian
							if known.votes >= VOTES_REQ:
								new_pedestrian = Pedestrian(known.x, known.y)
								self.unique_pedestrians.append(new_pedestrian)
								self.candidates.remove(known)

				# If a match still wasn't found, create a new candidate
				if matched == False:
					new_candidate = Candidate(found[0], found[1])
					self.candidates.append(new_candidate)
			self.prune()
			return len(self.unique_pedestrians)




