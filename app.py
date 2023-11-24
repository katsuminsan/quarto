from bottle import Bottle, route, run, static_file, request, redirect, response, HTTPResponse
from bottle import jinja2_template as template

import quarto

g = quarto.App()
app = Bottle()


@app.get('/static/<filePath:path>')
def index(filePath):
	return static_file(filePath, root='./static')
	
@app.route('/', method='GET')
def index():
	redirect('/bord')

# 盤を表示する
@app.route('/bord', method=['GET', 'POST'])
def bord():
	stat = g.get_status()
	
	return template('bord.html',
		main_area=stat['main_area'],
		hp_1=stat['hp_1'],
		hp_2=stat['hp_2'],
		present_stage=stat['present_stage'],
		turn=stat['turn'],
		status=stat['status']
	)

@app.route('/advance', method=['POST'])
def advance():
	stat = None
	data = request.json
	poll_uni = data['poll_uni']
	if isinstance(poll_uni, str):
		poll_uni = int(poll_uni)
	pos = data['pos']
	
	print(poll_uni, str(pos), g.phase, data['dbg'])
	
	if g.phase == 0:
		hp = [p.unique for p in g.hand_piece[g.turn_cnt % 2]]
		
		if poll_uni in hp:
			hp_idx = hp.index(poll_uni)
			g.present_poll(hp_idx)
	elif g.phase == 1:
		if g.bord.exist(pos) == 16:
			g.puton_poll(pos)
			if g.bord.check(pos):
				# game end
				pass
	
	body = g.get_status()
	r = HTTPResponse(status=200, body=body)
	r.set_header("Content-Type", "application/json")
	return r


if __name__ == '__main__':
	run(app=app, debug=True)
