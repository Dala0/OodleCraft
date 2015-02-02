#controls
from pyglet.window import key
from pyglet.window import mouse
from pyglet import event

def onAnyMovement(s):
	if not s.hasMovedSinceStartedClicking and s.mouse_action_start and s.aimpair:
		mas = s.mouse_action_start
		s.mouse_action_start = (mas[0],mas[1],mas[2],s.aimpair[3])
	s.hasMovedSinceStartedClicking = True
	

def game_on_key_press(s,symbol, modifiers):
	if s.menu == 0:
		if symbol == key.U:
			s.Undo()
		if symbol == key.A:
			s.playercontrol.x = 1
			onAnyMovement(s)
		if symbol == key.D:
			s.playercontrol.x = -1
			onAnyMovement(s)
		if symbol == key.W:
			s.playercontrol.z = 1
			onAnyMovement(s)
		if symbol == key.S:
			s.playercontrol.z = -1
			onAnyMovement(s)
		if symbol == key.G:
			s.SeedLand()
		if symbol == key.F:
			s.flying = not s.flying
		if symbol == key.SPACE:
			s.playercontrol.y = 1
			onAnyMovement(s)
		if symbol == key.LSHIFT:
			s.playercontrol.y = -1
			onAnyMovement(s)
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
		s.changeaim( - dx * rotScale, dy * rotScale )

VOLUME_MOD = key.MOD_CTRL

def game_on_mouse_press(s, x, y, buttons, modifiers):
	if s.menu == 1:
		sx = x - s.invx - s.invb
		sy = s.height - y - s.invy - s.invb
		if sx > 0 and sx < 40 * 15 and sy > 0 and sy < 40 * 9:
			iconx = sx/40
			icony = sy/40
			sx = sx - iconx*40
			sy = sy - icony*40
			if sx < 32 and sy < 32:
				#select a material based on this icon
				icon = iconx + icony * 15
				if icon > 0 and icon <= s.MAX_ID:
					s.plonk = icon
	if s.menu == 0:
		if s.aimpair:
			centre, vacancy, w,d = s.aimpair
			if buttons & mouse.LEFT:
				s.mouse_action_start = s.aimpair
				s.inDelete = True
			if buttons & mouse.RIGHT:
				s.mouse_action_start = s.aimpair
				s.inInsert = True
		if s.playercontrol.x == 0 and s.playercontrol.y == 0 and s.playercontrol.z == 0:
			s.hasMovedSinceStartedClicking = False
			
def tadd(a,b):
	return tuple(map(lambda t: t[0]+t[1],zip(a,b)))
def tsub(a,b):
	return tuple(map(lambda t: t[0]-t[1],zip(a,b)))
def mul(a): return a[0]*a[1]
irange = lambda x,y: range(min(x,y),max(x,y)+1)
brange = lambda x,y: range(min(x,y)-1,max(x,y)+2)
def virange( low, high ):
	for x in irange( int(low[0]), int(high[0]) ):
		for y in irange( int(low[1]), int(high[1]) ):
			for z in irange( int(low[2]), int(high[2]) ):
				yield (x,y,z)
def bvirange( low, high ):
	for x in brange( int(low[0]), int(high[0]) ):
		for y in brange( int(low[1]), int(high[1]) ):
			for z in brange( int(low[2]), int(high[2]) ):
				yield (x,y,z)

def game_on_mouse_release(s, x, y, buttons, modifiers):
	if s.menu == 0:
		if s.aimpair or s.hasMovedSinceStartedClicking:
			#if modifiers & VOLUME_MOD and s.mouse_action_start != None:
			if s.mouse_action_start != None:
				oc,ov,ow,od = s.mouse_action_start
				centre, vacancy,w,d = s.mouse_action_start
				if s.aimpair:
					centre, vacancy,w,d = s.aimpair
				world = s.worlds[w]
				updates = []
				if s.brushsize == 1:
					if ow == w:
						if buttons & mouse.LEFT:
							if s.mode == s.MODE_EDIT:
								if s.hasMovedSinceStartedClicking:
									centre = s.getInAirPoint()
								s.DebugLog("Deleting from "+repr(oc)+" to "+repr(centre))
								for pos in bvirange(oc,centre):
									updates.append(pos)
								s.StoreForUndo(world,updates)
								for pos in virange(oc,centre):
									if pos in world.space:
										del world.space[pos]
										s.c.send("d"+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
							if s.mode == s.MODE_PAINTING:
								s.DebugLog("Picking from "+repr(centre))
								s.plonk = world.space[centre]
						if buttons & mouse.RIGHT:
							plonk = s.plonk
							if s.mode == s.MODE_PAINTING: #painting
								if s.hasMovedSinceStartedClicking:
									centre = s.getInAirPoint()
								s.DebugLog("Painting over range "+repr(oc)+" to "+repr(centre))
								for pos in virange(oc,centre):
									if pos in world.space:
										updates.append(pos)
										world.space[pos] = plonk
										s.c.send("a"+str(plonk)+','+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
							if s.mode == s.MODE_EDIT:
								if s.hasMovedSinceStartedClicking:
									vacancy = s.getInAirPoint()
								s.DebugLog("Inserting from "+repr(ov)+" to "+repr(vacancy))
								for pos in bvirange(ov,vacancy):
									updates.append(pos)
								s.StoreForUndo(world,updates)
								for pos in virange(ov,vacancy):
									world.space[pos] = plonk
									s.c.send("a"+str(plonk)+','+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
				else:
					#brush size is greater than 1, just do one add/delete
					bs = s.brushsize
					vbs = (bs,bs,bs)
					reduction = 0.5
					limit = pow(bs-reduction,2)
					if s.mode == s.MODE_EDIT:
						if buttons & mouse.LEFT:
							s.DebugLog("Deleting a sphere at "+repr(centre)+" rad "+str(s.brushsize))
							for pos in bvirange( tsub(centre, vbs), tadd(centre, vbs) ):
								updates.append(pos)
							s.StoreForUndo(world,updates)
							for pos in virange( tsub(centre, vbs), tadd(centre, vbs) ):
								off = tsub(pos,centre)
								d2 = sum(map(mul, zip(off,off)))
								if d2 < limit:
									if pos in world.space:
										del world.space[pos]
										s.c.send("d"+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
						if buttons & mouse.RIGHT:
							s.DebugLog("Creating a sphere at "+repr(centre)+" rad "+str(s.brushsize))
							plonk = s.plonk
							for pos in bvirange( tsub(vacancy, vbs), tadd(vacancy, vbs) ):
								updates.append(pos)
							s.StoreForUndo(world,updates)
							for pos in virange( tsub(centre, vbs), tadd(centre, vbs) ):
								off = tsub(pos,centre)
								d2 = sum(map(mul, zip(off,off)))
								if d2 < limit:
									world.space[pos] = plonk
									s.c.send("a"+str(plonk)+','+str(pos[0])+','+str(pos[1])+','+str(pos[2])+','+str(w))
					if s.mode == s.MODE_PAINTING:
						if buttons & mouse.RIGHT:
							s.DebugLog("Creating a sphere at "+repr(centre)+" rad "+str(s.brushsize))
							plonk = s.plonk
							bext = (s.brushsize,s.brushsize,s.brushsize)
							for pos in virange(tsub(vacancy,bext),tadd(vacancy,bext)):
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
						if buttons & mouse.LEFT:
							s.DebugLog("Picking from "+repr(centre))
							s.plonk = world.space[centre]
				if len(updates) > 0:
					s.refreshFor(world,updates)
			s.mouse_action_start = None
			s.inInsert = False
			s.inDelete = False
				
def game_on_mouse_scroll(s,x, y, scroll_x, scroll_y):
	s.brushsize = min( max( 1, s.brushsize + scroll_y ), 8 );
	s.SetMessage( s, "Brush Size : "+str(s.brushsize ) )
	pass

