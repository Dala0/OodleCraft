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

mouse_action_start = None

def game_on_mouse_press(s, x, y, buttons, modifiers):
	global mouse_action_start
	if s.mode == 0:
		if s.aimpair:
			centre, vacancy = s.aimpair
			if buttons & mouse.LEFT:
				if centre in s.space:
					del s.space[centre]
					mouse_action_start = (centre,vacancy,-1)
					s.c.send("d"+str(centre[0])+','+str(centre[1])+','+str(centre[2]))
					s.updateWorldList(s,centre)
				else:
					print "Cell ",centre," not in space"
			if buttons & mouse.RIGHT:
				plonk = s.plonk
				mouse_action_start = (centre,vacancy,plonk)
				s.space[vacancy] = plonk
				s.c.send("a"+str(plonk)+','+str(vacancy[0])+','+str(vacancy[1])+','+str(vacancy[2]))
				s.updateWorldList(s,vacancy)
			
def tsub(a,b):
	return tuple(map(lambda t: t[0]-t[1],zip(a,b)))
irange = lambda x,y: range(min(x,y),max(x,y)+1)

def game_on_mouse_release(s, x, y, buttons, modifiers):
	global mouse_action_start
	if s.mode == 0:
		if s.aimpair:
			if mouse_action_start != None:
				oc,ov,op = mouse_action_start
				centre, vacancy = s.aimpair
				oproj = tuple(map(lambda t: t[0]-t[1],zip(ov,oc)))
				proj = tuple(map(lambda t: t[0]-t[1],zip(vacancy,centre)))
				if oproj == proj:
					updates = []
					if buttons & mouse.LEFT:
						plonk = s.plonk
						for x in irange( oc[0],centre[0] ):
							for y in irange( oc[1],centre[1] ):
								for z in irange( oc[2],centre[2] ):
									pos = (x,y,z)
									if pos in s.space:
										del s.space[pos]
										s.c.send("d"+str(x)+','+str(y)+','+str(z))
										updates.append(pos)
									#s.updateWorldList(s,pos)
					if buttons & mouse.RIGHT:
						plonk = s.plonk
						for x in irange( ov[0],vacancy[0] ):
							for y in irange( ov[1],vacancy[1] ):
								for z in irange( ov[2],vacancy[2] ):
									pos = (x,y,z)
									s.space[pos] = plonk
									s.c.send("a"+str(plonk)+','+str(x)+','+str(y)+','+str(z))
									updates.append(pos)
									#s.updateWorldList(s,pos)
					if len(updates) > 0:
						s.refreshFor(s,updates)
				mouse_action_start = None
				
def game_on_mouse_scroll(s,x, y, scroll_x, scroll_y):
	s.changeMaterial( s, scroll_y)

