#controls
from pyglet.window import key
from pyglet.window import mouse

def game_on_key_press(scope,symbol, modifiers):
	if scope['mode'] == 0:
		if symbol == key.A:
			scope['playercontrol'].x = 1
		if symbol == key.D:
			scope['playercontrol'].x = -1
		if symbol == key.W:
			scope['playercontrol'].z = 1
		if symbol == key.S:
			scope['playercontrol'].z = -1
		if symbol == key.SPACE:
			scope['playercontrol'].y = 1
		if symbol == key.LSHIFT:
			scope['playercontrol'].y = -1
		if symbol == key._1:
			scope['plonk'] = 1
		if symbol == key._2:
			scope['plonk'] = 2
		if symbol == key._3:
			scope['plonk'] = 3
		if symbol == key.LEFT:
			scope['changeMaterial'](-1)
		if symbol == key.RIGHT:
			scope['changeMaterial'](1)
	if symbol == key.TAB:
		scope['switchMode']()

def game_on_key_release(scope,symbol, modifiers):
	if scope['mode'] == 0:
		if symbol == key.A or symbol == key.D:
			scope['playercontrol'].x = 0
		if symbol == key.W or symbol == key.S:
			scope['playercontrol'].z = 0
		if symbol == key.SPACE or symbol == key.LSHIFT:
			scope['playercontrol'].y = 0

def game_on_mouse_motion( scope, x, y, dx, dy ):
	rotScale = 0.0025
	if scope['mode'] == 0:
		scope['changeaim'](- dx * rotScale, dy * rotScale )

def game_on_mouse_press(scope, x, y, buttons, modifiers):
	if scope['mode'] == 0:
		if scope['aimpair']:
			centre, vacancy = scope['aimpair']
			if buttons & mouse.LEFT:
				del scope['space'][centre]
				scope['c'].send("d"+str(centre[0])+','+str(centre[1])+','+str(centre[2]))
				scope['updateWorldList'](centre)
			if buttons & mouse.RIGHT:
				plonk = scope['plonk']
				scope['space'][vacancy] = plonk
				scope['c'].send("a"+str(plonk)+','+str(vacancy[0])+','+str(vacancy[1])+','+str(vacancy[2]))
				scope['updateWorldList'](vacancy)
			
def game_on_mouse_scroll(scope,x, y, scroll_x, scroll_y):
	scope['changeMaterial'](scroll_y)

