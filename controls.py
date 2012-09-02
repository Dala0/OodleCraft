#controls
from pyglet.window import key
from pyglet.window import mouse

def game_on_key_press(s,symbol, modifiers):
	if s.mode == 0:
		if symbol == key.U:
			s.Undo()
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
VOLUME_MOD = key.MOD_CTRL

def game_on_mouse_press(s, x, y, buttons, modifiers):
	global mouse_action_start
	if s.mode == 1:
		sx = x - s.invx - s.invb
		sy = s.height - y - s.invy - s.invb
		print "x,y = ",sx,",",sy
		if sx > 0 and sx < 40 * 8 and sy > 0 and sy < 40 * 8:
			iconx = sx/40
			icony = sy/40
			print "iconx,icony = ",iconx,",",icony
			sx = sx - iconx*40
			sy = sy - icony*40
			print "sx,sy = ",sx,",",sy
			if sx < 32 and sy < 32:
				#select a material based on this icon
				icon = iconx + icony * 8
				print "Set plonk to ",icon
				if icon > 0 and icon <= s.MAX_ID:
					s.plonk = icon
	if s.mode == 0:
		if s.aimpair:
			centre, vacancy = s.aimpair
			if buttons & mouse.LEFT:
				if centre in s.space:
					#del s.space[centre]
					if True: #modifiers & VOLUME_MOD:
						mouse_action_start = (centre,vacancy)
					#s.c.send("d"+str(centre[0])+','+str(centre[1])+','+str(centre[2]))
					#s.updateWorldList(s,centre)
			if buttons & mouse.RIGHT:
				plonk = s.plonk
				if True: #modifiers & VOLUME_MOD:
					mouse_action_start = (centre,vacancy)
				#s.space[vacancy] = plonk
				#s.c.send("a"+str(plonk)+','+str(vacancy[0])+','+str(vacancy[1])+','+str(vacancy[2]))
				#s.updateWorldList(s,vacancy)
			
def tsub(a,b):
	return tuple(map(lambda t: t[0]-t[1],zip(a,b)))
irange = lambda x,y: range(min(x,y),max(x,y)+1)
brange = lambda x,y: range(min(x,y)-1,max(x,y)+2)

def game_on_mouse_release(s, x, y, buttons, modifiers):
	global mouse_action_start
	if s.mode == 0:
		if s.aimpair:
			#if modifiers & VOLUME_MOD and mouse_action_start != None:
			if mouse_action_start != None:
				oc,ov = mouse_action_start
				centre, vacancy = s.aimpair
				oproj = tuple(map(lambda t: t[0]-t[1],zip(ov,oc)))
				proj = tuple(map(lambda t: t[0]-t[1],zip(vacancy,centre)))
				if True: #oproj == proj:
					updates = []
					if buttons & mouse.LEFT:
						plonk = s.plonk
						for x in brange( oc[0],centre[0] ):
							for y in brange( oc[1],centre[1] ):
								for z in brange( oc[2],centre[2] ):
									pos = (x,y,z)
									updates.append(pos)
						s.StoreForUndo(updates)
						for x in irange( oc[0],centre[0] ):
							for y in irange( oc[1],centre[1] ):
								for z in irange( oc[2],centre[2] ):
									pos = (x,y,z)
									if pos in s.space:
										del s.space[pos]
										s.c.send("d"+str(x)+','+str(y)+','+str(z))
					if buttons & mouse.RIGHT:
						plonk = s.plonk
						for x in brange( ov[0],vacancy[0] ):
							for y in brange( ov[1],vacancy[1] ):
								for z in brange( ov[2],vacancy[2] ):
									pos = (x,y,z)
									updates.append(pos)
						s.StoreForUndo(updates)
						for x in irange( ov[0],vacancy[0] ):
							for y in irange( ov[1],vacancy[1] ):
								for z in irange( ov[2],vacancy[2] ):
									pos = (x,y,z)
									s.space[pos] = plonk
									s.c.send("a"+str(plonk)+','+str(x)+','+str(y)+','+str(z))
					if len(updates) > 0:
						s.refreshFor(s,updates)
			mouse_action_start = None
				
def game_on_mouse_scroll(s,x, y, scroll_x, scroll_y):
	#s.changeMaterial( s, scroll_y)
	pass

