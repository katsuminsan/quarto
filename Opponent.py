

class opponent():
	levels = [1, 2, 3, 4, 5]
	def __init__(self, area, hp1, hp2, pre_p, level=5):
		self.init_inside_info(area, hp1, hp2, pre_p)
		self.level = opponent.levels[level]
		
	def init_inside_info(self, area, hp1, hp2, pre_p):
		self.area = area
		self.hp1 = hp1
		self.hp2 = hp2
		self.pre_p = pre_p
		
	def select_pos(self):
		pass
		
	def choise_poll(self):
		pass

