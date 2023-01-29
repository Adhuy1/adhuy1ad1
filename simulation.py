import math


class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y
    self.lx, self.ly = x, y
    self.pinned = False
    self.drag = False
  
  def update(self, ax = 0, ay = 0.5, max_a = 15):
    if self.pinned == False:
      vx, vy = min(self.x - self.lx, max_a), min(self.y - self.ly, max_a)
      
      if self.x > screen_w:
        self.x = screen_w
        vx *= -0.3
      elif self.x < 0:
        self.x = 0
        vx *= -0.3
      if self.y > screen_h:
        self.y = screen_h
        vy *= -0.3
      elif self.y < 0:
        self.y = 0
        vy *= -0.3
      
      nx, ny = self.x + vx + ax, self.y + vy + ay
      
      self.lx, self.ly = self.x, self.y
      self.x, self.y = nx, ny


class Link:
  def __init__(self, p1, p2, d, t):
    self.p1, self.p2, self.d, self.t = p1, p2, d, t
    self.broken = False
  
  def solve(self):
    dist_x = self.p1.x - self.p2.x
    dist_y = self.p1.y - self.p2.y
    
    dist = math.dist((self.p1.x,self.p1.y), (self.p2.x,self.p2.y))
    
    if dist > self.t:
      self.broken = True
    else:
      diff = (self.d - dist)/max(dist,0.1)
      
      dx = dist_x * 0.5 * diff
      dy = dist_y * 0.5 * diff
      
      if self.p1.pinned == False and self.p1.drag == False:
        self.p1.x += dx
        self.p1.y += dy
      if self.p2.pinned == False and self.p1.drag == False:
        self.p2.x -= dx
        self.p2.y -= dy


class Cloth:
  def __init__(self, size=15, l=10, tear=40, offset=(0,0), screen_size=(500,300)):
    global screen_w, screen_h
    screen_w, screen_h = screen_size
    
    self.points = [[Point(x*l+offset[0],y*l+offset[1]) for x in range(size)] for y in range(size)]
    
    self.links = []
    
    for y, row in enumerate(self.points):
      for x, point in enumerate(row):
        if y == 0:
          point.pinned = True
        else:
          if x != 0:
            self.links.append(Link(point, row[x-1], l, tear))
          
          self.links.append(Link(point, self.points[y-1][x], l, tear))
    
    self.dragging = []
  
  def start_drag(self, pos, drag_radius=20):
    for points in self.points:
      for point in points:
        if point.pinned == False:
          if math.dist((point.x,point.y), pos) < drag_radius:
            point.drag = True
            point.drag_pos = (point.x, point.y)
            
            self.dragging.append(point)
  
  def end_drag(self):
    for point in self.dragging:
      point.drag = False
    
    self.dragging.clear()
  
  def drag(self, dx, dy):
    for point in self.dragging:
      if point.drag == True:
        point.x = point.drag_pos[0] + dx
        point.y = point.drag_pos[1] + dy
  
  def update(self, iterations=3):
    for _ in range(iterations):
      for link in self.links:
        if link.broken == True:
          self.links.remove(link)
        else:
          link.solve()
    
    for points in self.points:
      for point in points:
        point.update()