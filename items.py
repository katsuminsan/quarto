
class poll():
	def __init__(self, unique=16):
		self.unique = unique
	def __str__(self):
		return f'{self.unique:05b}'
	
class bord():
	def __init__(self):
		self.aria = [[poll(16) for i in range(4)] for ii in range(4)]
		
	def exist(self, coordinate):
		# coordinate: left_top (0,0)
		return self.aria[coordinate[0]][coordinate[1]].unique
		
		
	def puton(self, p, coordinate):
		# coordinate: left_top (0,0)
		self.aria[coordinate[0]][coordinate[1]] = p
		
	def binlist_and(self, bin_l):
		l = [j for j in bin_l if j<=15]
		
		if len(l) == 4:
			rev_l = [int(f'{~j&0b1111:04b}',2) for j in bin_l if j<=15]
			buf = '&'.join([str(j) for j in l])
			rev_buf = '&'.join([str(j) for j in rev_l])
		else:
			buf = 'False'
			rev_buf = 'False'
		
		result = any([
			bool(eval(buf)),
			bool(eval(rev_buf))
			])
		
		return result
		
	def all_check(self):
		# all lines check.
		# The return value has a boolean
		# and the status of each line.
		
		ar = self.aria
		bool_chks = {}
		
		# row_chk
		chk_lst = []
		for i, r in enumerate(ar):
			chk_lst = [int(str(ir),2) for ir in r]
			bool_chks[f'r{i}'] = self.binlist_and(chk_lst)
		
		# col_chk
		rev_ar = list(zip(*ar))
		chk_lst = []
		for i, r_r in enumerate(rev_ar):
			chk_lst = [int(str(ir),2) for ir in r_r]
			bool_chks[f'c{i}'] = self.binlist_and(chk_lst)
		
		# x_chk
		x_ar = [ar[c][c] for c in range(4)]
		chk_lst = [int(str(ir),2) for ir in x_ar]
		bool_chks['x_dwn'] = self.binlist_and(chk_lst)
		
		rev_x_ar = [ar[c][-c-1] for c in range(4)]
		chk_lst = [int(str(ir),2) for ir in rev_x_ar]
		bool_chks['x_up'] = self.binlist_and(chk_lst)
		
		# all_chk
		return any(bool_chks.values()), bool_chks
		
	def check(self, act_point):
		# act_point (r, c) orizins (0,0)
		
		ar = self.aria
		bool_chks = []
		
		# row_chk
		chk_lst = [int(str(ir),2) for ir in ar[act_point[0]]]
		bool_chks.append(self.binlist_and(chk_lst))
		
		# col_chk
		rev_ar = list(zip(*ar))
		chk_lst = []
		chk_lst = [int(str(ir),2) for ir in rev_ar[act_point[1]]]
		bool_chks.append(self.binlist_and(chk_lst))
		
		# x_chk
		if act_point[0]-act_point[1] == 0:
			# \ライン
			x_ar = [ar[c][c] for c in range(4)]
			chk_lst = [int(str(ir),2) for ir in x_ar]
			bool_chks.append(self.binlist_and(chk_lst))
			
		if sum(act_point)==3:
			# /ライン
			rev_x_ar = [ar[c][-c-1] for c in range(4)]
			chk_lst = [int(str(ir),2) for ir in rev_x_ar]
			bool_chks.append(self.binlist_and(chk_lst))
		
		# chk
		return any(bool_chks)
		
	def show(self):
		s_ar = ''
		for r in self.aria:
			s_ar += str(' '.join([str(i) for i in r]) + '\n')
		print(s_ar)


if __name__ == '__main__':
	polls = [poll(i) for i in range(17)]
	b = bord()
	
	b.puton(polls[0], (0,3))
	b.puton(polls[4], (1,2))
	b.puton(polls[5], (2,1))
	b.puton(polls[9], (2,2))
	b.puton(polls[13], (3,0))
	b.show()
	print(f'game end := {b.check((3,0))}')

