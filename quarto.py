import items

def radix(n, base):
	minus = '' if n>=0 else '-'
	buf = ''
	# 10進数 → n進数
	if n != 0:
		while n > 0:
			buf = str(n%base) + buf
			n //= base
	else:
		buf = '0'
	
	return minus + buf
	
def roll_to_zero(num, add, base=2):
	# The argument "base" is a number that is replaced with 0 when reached.
	# When "base=2", the range of the ones digit is "0 to 1".
	numadd = abs(num + add)
	# rtn = int(radix(numadd, base=base)[-1])
	rtn = numadd % base
	return int(rtn)

class App():
	def __init__(self):
		self.init_game()
		self.users = ['Me', 'enemy']
		
	def init_game(self):
		_polls = [items.poll(i) for i in range(16)]
		self.bord = items.bord()
		self.hand_piece = (_polls[:8], _polls[8:])
		self.present_piece = items.poll()
		self.turn_cnt = 1
		self._ph = 0
		
	@property
	def phase(self):
		rtz = roll_to_zero(self._ph, 0, base=2)
		return rtz
		
	@phase.setter
	def phase(self, p):
		self._ph = p
		
	def phase_up(self, cnt=1):
		self._ph += cnt
		
	def puton_poll(self, position):
		obj_poll = self.present_piece
		self.present_piece = items.poll()
		self.bord.puton(obj_poll, position)
		self.phase_up()
		
	def present_poll(self, poll_index):
		p_poll = self.hand_piece[self.turn_cnt%2].pop(poll_index)
		self.present_piece = p_poll
		self.phase_up()
		self.turn_cnt += 1
		
	def get_status(self):
		
		if self.bord.all_check()[0]:
			st = f'finished - winner is {self.users[self.turn_cnt%2]}'
		elif self.turn_cnt == 17 and self.phase == 0 :
			st = 'finished - drow'
		else:
			st = f'{self.users[self.turn_cnt%2]} turn'
		
		return {
			'main_area': [[p.unique for p in row] for row in self.bord.aria],
			'hp_1': [p.unique for p in self.hand_piece[0]],
			'hp_2': [p.unique for p in self.hand_piece[1]],
			'present_stage': self.present_piece.unique,
			'turn': self.turn_cnt,
			'phase': self.phase,
			'status': st
		}
		
	def cui_preview(self):
		stat = self.get_status()
		
		print('')
		print('')
		print('')
		print('')
		print(f'+++ {self.users[1]} +++')
		print([str(p) for p in self.hand_piece[1]])
		print('')
		print(f'                       present poll :=> {self.present_piece}')
		self.bord.show()
		print('')
		print(f'+++ {self.users[0]} +++')
		print([str(p) for p in self.hand_piece[0]])
		print('')
		print(self.users[stat['turn']%2] + ' turn')
		
		
if __name__=='__main__':
	
	import re
	app = App()
	print(app.get_status()['main_area'])
	
	while True:
		app.cui_preview()
		if app.phase == 0:
			
			poll_num = int(input(':= choise present poll. '))
			
			hp_pcnt = len(app.hand_piece[app.turn_cnt % 2])
			if 1 <= poll_num and poll_num <= hp_pcnt:
				p_poll = poll_num - 1
				app.present_poll(p_poll)
			else:
				print(f'err: present poll is 1 ~ {hp_pcnt}')
				
		elif app.phase == 1:
			
			choise_pos = input(':= choise put on to bord position. ')
			
			if re.fullmatch(r'[0-3],[0-3]', choise_pos) is not None:
				pos = [int(cp) for cp in choise_pos.split(',')]
				
				if app.bord.exist(pos) == 16:
					app.puton_poll(pos)
					if 'finish' in app.get_status()['status']:
						break
				else:
					print(f'err: There is already a pole in {choise_pos}')
					
			else:
				print('err: position is (0,0) ~ (3,3)')
				
	app.cui_preview()
	print(app.get_status())
	print('*** end game ***')
