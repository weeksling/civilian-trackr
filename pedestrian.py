import numpy as np

_id = 0

class Pedestrian:
  def __init__(self, x,y):
    global _id
    self.x = x
    self.y = y
    self.id = _id
    _id = _id + 1

  def update_location(self, x, y):
    if abs(x-self.x) < 60 and abs(y-self.y) < 60
      self.x = 0.6*self.x + 0.4*x
      self.y = 0.6*self.y + 0.4*y

  def get_ID():
    return self.id

  def get_location():
    return (self.x, self.y)
