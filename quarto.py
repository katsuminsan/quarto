import items
import Opponent

def polls_index_find(poll_l, poll_x):
	# l:= list obj, x:= search value
	l = [str(i) for i in poll_l]
	x = str(poll_x)
	return l.index(x) if x in l else -1

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

def is_valid_poslist(data):
	return (
		isinstance(data, (list, tuple)) and
		len(data) == 2 and
		all(isinstance(x, int) and 0 <= x <= 3 for x in data)
	)

class App():
	def __init__(self):
		self.locals_handpiece = False
		self.init_game()
		self.users = ['Me', 'enemy']
		self.vs_mode = 'cpu' # cpu or pvp
		self.oppo = Opponent.Opponent(level='hard') # 置く時の判定だけ
	def init_game(self):
		_polls = [items.poll(i) for i in range(16)]
		self.bord = items.bord()
		if self.locals_handpiece:
			self.hand_piece = (_polls[:8], _polls[8:])
		else:
			self.hand_piece = _polls
		self.present_piece = items.poll()
		self.turn_cnt = 1
		self._ph = 0
		
	@property
	def phase(self):
		return self._ph % 2
		
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
		if self.locals_handpiece:
			p_poll = self.hand_piece[self.turn_cnt%2].pop(poll_index)
		else:
			p_poll = self.hand_piece.pop(poll_index)
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
		
		if self.locals_handpiece:
			res = {
				'vs_mode': self.vs_mode,
				'main_area': [[p.unique for p in row] for row in self.bord.aria],
				'hp_1': [p.unique for p in self.hand_piece[0]],
				'hp_2': [p.unique for p in self.hand_piece[1]],
				'present_stage': self.present_piece.unique,
				'turn': self.turn_cnt,
				'phase': self.phase,
				'status': st
			}
		else:
			res = {
				'vs_mode': self.vs_mode,
				'main_area': [[p.unique for p in row] for row in self.bord.aria],
				'hp': [p.unique for p in self.hand_piece],
				'present_stage': self.present_piece.unique,
				'turn': self.turn_cnt,
				'phase': self.phase,
				'status': st
			}
		
		return res
		
	def cui_preview(self):
		stat = self.get_status()
		
		print('')
		print('<___________________________________>')
		print('')
		print(f'+++ {self.users[1]} +++')
		if self.locals_handpiece:
			print([str(i+1) + ':' + str(p)[1:] for i, p in enumerate(self.hand_piece[1])])
		else:
			print('')
			print('')
			print('-- hand_piese area --')
			print([str(i+1) + ':' + str(p)[1:] for i, p in enumerate(self.hand_piece)])
			print('---------------------')
		print('')
		_prep = str(self.present_piece)[1:] if self.present_piece.unique <= 15 else '----'
		
		print(f'                  present poll :=> {_prep}')
		
		self.bord.show()
		
		print('')
		print(f'+++ {self.users[0]} +++')
		if self.locals_handpiece:
			print([str(i+1) + ':' + str(p)[1:] for i, p in enumerate(self.hand_piece[0])])
		else:
			print('')
		print('')
		print(' @ ' + self.users[stat['turn']%2] + ' turn')
		print('')
		print('')

if __name__=='__main__':
	
	import re
	app = App()
	
	# print(app.get_status()['main_area'])
	'''
	app.present_poll(1)
	app.puton_poll((0,0))
	app.present_poll(2)
	app.puton_poll((2,1))
	app.present_poll(3)
	app.puton_poll((3,2))
	
	g_st = app.get_status()
	print(g_st)
	'''
	
	#op = opponent(g_st['main_area'], g_st['hp_1'], g_st['hp_2'], g_st['present_stage'], level=5)
	
	#op.show()
	# print(op.scoreboard)
	
	def cpuAct_phase_0(app):
		print('ai loading...')
		remaining = app.oppo._get_remaining_pieces(app.bord)
		present = app.oppo.choose_next_piece(app.bord, remaining)
		print(f'aiならば、駒:{str(present)[1:]} を渡す')
		print('')
		return polls_index_find(app.hand_piece, present) + 1
		
	def cpuAct_phase_1(app):
		print('ai loading...')
		coord = app.oppo.choose_placement(app.bord, app.present_piece)
		print(f'aiならば、{coord}に 駒:{str(app.present_piece)[1:]} を置く')
		print('')
		return coord
		
	while True:
		app.cui_preview()
		if app.phase == 0:
			
			if app.vs_mode == 'cpu' and app.turn_cnt %2 == 1:
				poll_num = cpuAct_phase_0(app)
				
			elif app.vs_mode == 'pvp' or app.turn_cnt %2 ==0:
				poll_num = int(input(' := choise present poll.\n '))
			
			if app.locals_handpiece:
				hp_pcnt = len(app.hand_piece[app.turn_cnt % 2])
			else:
				hp_pcnt = len(app.hand_piece)
				
			if 1 <= poll_num and poll_num <= hp_pcnt:
				p_poll = poll_num - 1
				app.present_poll(p_poll)
			else:
				print('')
				print('')
				print(f'err: present poll is 1 ~ {hp_pcnt}. {poll_num} is error')
				
				
		elif app.phase == 1:
			if app.vs_mode == 'cpu' and app.turn_cnt %2 == 1:
				choise_pos = cpuAct_phase_1(app)
				if is_valid_poslist(choise_pos):
					pos = choise_pos
				else:
					print('')
					print('')
					print('err: position is (0,0) ~ (3,3)')
					continue
					
			elif app.vs_mode == 'pvp' or app.turn_cnt %2 == 0:
				choise_pos = input(' := choise put on to bord position.\n •(row_num, column_num)\n •zero start\n ')
				
				if re.fullmatch(r'[0-3],[0-3]', choise_pos) is not None:
					pos = [int(cp) for cp in choise_pos.split(',')]
				else:
					print('')
					print('')
					print('err: position is (0,0) ~ (3,3)')
					continue
					
			if app.bord.exist(pos) == 16:
				app.puton_poll(pos)
				if 'finish' in app.get_status()['status']:
					break
			else:
				print('')
				print('')
				print(f'err: There is already a pole in {choise_pos}')
				
	# app.cui_preview()
	# print(app.get_status())
	print('*** end game ***')
