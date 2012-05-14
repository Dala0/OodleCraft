#controls
from pyglet.window import key
from pyglet.window import mouse

def game_on_key_press(s,symbol, modifiers):
	if s.mode == 0:
		if symbol == key.A:
			s.playercontrol.x = 1
		if symbol == key.D:
			s.playercontrol.x = -1
		if symbol == key.W:
			s.playercontrol.z = 1
		if symbol == key.S:
			s.playercontrol.z = -1
		if symbol == key.F:
			s.flying = not s.flying
		if symbol == key.SPACE:
			s.playercontrol.y = 1
		if symbol == key.LSHIFT:
			s.playercontrol.y = -1
		if symbol == key._1:
			s.plonk = 1
		if symbol == key._2:
			s.plonk = 2
		if symbol == key._3:
			s.plonk = 3
		if symbol == key.LEFT:
			s.changeMaterial(-1)
		if symbol == key.RIGHT:
			s.changeMaterial(1)
	if symbol == key.TAB:
		s.switchMode(s)

def game_on_key_release(s,symbol, modifiers):
	if s.mode == 0:
		if symbol == key.A or symbol == key.D:
			s.playercontrol.x = 0
		if symbol == key.W or symbol == key.S:
			s.playercontrol.z = 0
		if symbol == key.SPACE or symbol == key.LSHIFT:
			s.playercontrol.y = 0

def game_on_mouse_motion( s, x, y, dx, dy ):
	rotScale = 0.0025
	if s.mode == 0:
		s.changeaim( s, - dx * rotScale, dy * rotScale )

def game_on_mouse_press(s, x, y, buttons, modifiers):
	if s.mode == 0:
		if s.aimpair:
			centre, vacancy = s.aimpair
			if buttons & mouse.LEFT:
				del s.space[centre]
				s.c.send("d"+str(centre[0])+','+str(centre[1])+','+str(centre[2]))
				s.updateWorldList(s,centre)
			if buttons & mouse.RIGHT:
				plonk = s.plonk
				s.space[vacancy] = plonk
				s.c.send("a"+str(plonk)+','+str(vacancy[0])+','+str(vacancy[1])+','+str(vacancy[2]))
				s.updateWorldList(s,vacancy)
			
def game_on_mouse_scroll(s,x, y, scroll_x, scroll_y):
	s.changeMaterial( s, scroll_y)

