#controls
from pyglet.window import key
from pyglet.window import mouse
from pyglet import event

def game_on_key_press(s,symbol, modifiers):
	if s.menu == 0:
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
		if symbol == key.G:
			s.SeedLand()
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
		s.switchMode()
	if symbol == key.E:
		s.toggleMenu()
	if symbol == key.N:
		c = s.worlds.index(s.currentWorld)
		c = (1+c)%len(s.worlds)
		s.currentWorld = s.worlds[c]
	#if symbol == key.ESCAPE:
		#s.toggleMenu()
		#return event.EVENT_HANDLED

def game_on_key_release(s,symbol, modifiers):
	if s.menu == 0:
		if symbol == key.A or symbol == key.D:
			s.playercontrol.x = 0
		if symbol == key.W or symbol == key.S:
			s.playercontrol.z = 0
		if symbol == key.SPACE or symbol == key.LSHIFT:
			s.playercontrol.y = 0

def game_on_mouse_motion( s, x, y, dx, dy ):
	rotScale = 0.0025
	if s.menu == 0:
		s.changeaim( s, - dx * rotScale, dy * rotScale )

mouse_action_start = None
VOLUME_MOD = key.MOD_CTRL

def game_on_mouse_press(s, x, y, buttons, modifiers):
	global mouse_action_start
	if s.menu == 1:
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
	if s.menu == 0:
		if s.aimpair:
			centre, vacancy, w = s.aimpair
			if buttons & mouse.LEFT:
				mouse_action_start = s.aimpair
			if buttons & mouse.RIGHT:
				mouse_action_start = s.aimpair
			
def tadd(a,b):
	return tuple(map(lambda t: t[0]+t[1],zip(a,b)))
def tsub(a,b):
	return tuple(map(lambda t: t[0]-t[1],zip(a,b)))
irange = lambda x,y: range(min(x,y),max(x,y)+1)
brange = lambda x,y: range(min(x,y)-1,max(x,y)+2)
def vrange( low, high ):
	for x in irange( int(low[0]), int(high[0]) ):
		for y in irange( int(low[1]), int(high[1]) ):
			for z in irange( int(low[2]), int(high[2]) ):
				yield (x,y,z)
def bvrange( low, high ):
	for x in brange( int(low[0]), int(high[0]) ):
		for y in brange( int(low[1]), int(high[1]) ):
			for z in brange( int(low[2]), int(high[2]) ):
				yield (x,y,z)

def game_on_mouse_release(s, x, y, buttons, modifiers):
	global mouse_action_start
	if s.menu == 0:
		if s.aimpair:
			#if modifiers & VOLUME_MOD and mouse_action_start != None:
			if mouse_action_start != None:
				oc,ov,ow = mouse_action_start
				centre, vacancy,w = s.aimpair
				world = s.worlds[w]
				updates = []
				if s.brushsize == 1:
					if ow == w:
						if buttons & mouse.LEFT:
							if s.mode == 0:
								for pos in bvrange(oc,centre):
									updates.append(pos)
								s.StoreForUndo(world,updates)
								for pos in vrange(oc,centre):
									if pos in world.space:
										del world.space[pos]
										s.c.send("d"+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
							if s.mode == 1:
								s.plonk = world.space[centre]
						if buttons & mouse.RIGHT:
							plonk = s.plonk
							if s.mode == 1: #painting
								for pos in vrange(oc,centre):
									if pos in world.space:
										updates.append(pos)
										world.space[pos] = plonk
										s.c.send("a"+str(plonk)+','+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
							if s.mode == 0:
								for pos in bvrange(ov,vacancy):
									updates.append(pos)
								s.StoreForUndo(world,updates)
								for pos in vrange(ov,vacancy):
									world.space[pos] = plonk
									s.c.send("a"+str(plonk)+','+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
				else:
					#brush size is greater than 1, just do one add/delete
					bs = s.brushsize
					reduction = 0.5
					limit = pow(bs-reduction,2)
					if s.mode == 0:
						if buttons & mouse.LEFT:
							for x in brange( centre[0]-s.brushsize,centre[0]+s.brushsize ):
								for y in brange( centre[1]-s.brushsize,centre[1]+s.brushsize ):
									for z in brange( centre[2]-s.brushsize,centre[2]+s.brushsize ):
										pos = (x,y,z)
										updates.append(pos)
							s.StoreForUndo(world,updates)
							for x in irange( centre[0]-s.brushsize,centre[0]+s.brushsize ):
								x2 = pow(x - centre[0],2)
								for y in irange( centre[1]-s.brushsize,centre[1]+s.brushsize ):
									y2 = pow(y - centre[1],2)
									for z in irange( centre[2]-s.brushsize,centre[2]+s.brushsize ):
										z2 = pow(z - centre[2],2)
										if x2+y2+z2 < limit:
											pos = (x,y,z)
											if pos in world.space:
												del world.space[pos]
												s.c.send("d"+str(x)+','+str(y)+','+str(z)+','+str(w))
						if buttons & mouse.RIGHT:
							plonk = s.plonk
							for x in brange( vacancy[0]-s.brushsize,vacancy[0]+s.brushsize ):
								for y in brange( vacancy[1]-s.brushsize,vacancy[1]+s.brushsize ):
									for z in brange( vacancy[2]-s.brushsize,vacancy[2]+s.brushsize ):
										pos = (x,y,z)
										updates.append(pos)
							s.StoreForUndo(world,updates)
							for x in irange( vacancy[0]-s.brushsize,vacancy[0]+s.brushsize ):
								x2 = pow(x - vacancy[0],2)
								for y in irange( vacancy[1]-s.brushsize,vacancy[1]+s.brushsize ):
									y2 = pow(y - vacancy[1],2)
									for z in irange( vacancy[2]-s.brushsize,vacancy[2]+s.brushsize ):
										z2 = pow(z - vacancy[2],2)
										if x2+y2+z2 < limit:
											pos = (x,y,z)
											world.space[pos] = plonk
											s.c.send("a"+str(plonk)+','+str(x)+','+str(y)+','+str(z)+','+str(w))
					if s.mode == 1:
						if buttons & mouse.RIGHT:
							plonk = s.plonk
							bext = (s.brushsize,s.brushsize,s.brushsize)
							for pos in vrange(tsub(vacancy,bext),tadd(vacancy,bext)):
								if pos in world.space:
									d = tsub(pos,vacancy)
									d = reduce(lambda a,b: a+b,map(lambda t: t * t, d))
									if d < limit:
										updates.append(pos)
							s.StoreForUndo(world,updates)
							for pos in updates:
								if pos in world.space:
									world.space[pos] = plonk
									s.c.send("a"+str(plonk)+','+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
				if len(updates) > 0:
					s.refreshFor(s,world,updates)
			mouse_action_start = None
				
def game_on_mouse_scroll(s,x, y, scroll_x, scroll_y):
	s.brushsize = min( max( 1, s.brushsize + scroll_y ), 32 );
	s.SetMessage( s, "Brush Size : "+str(s.brushsize ) )
	#s.changeMaterial( s, scroll_y)
	pass

