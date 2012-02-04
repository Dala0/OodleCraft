from pyglet.gl import *
from pyglet import image
from pyglet.window import key
from pyglet.window import mouse
from pyglet import font
from pyglet.font import GlyphString

from math import * # trigonometry
from vec import *
from geom import *
import pickle
from glPrims import *
from assets import *
from materials import *
from worldgen import *

import netcore
c = netcore.netcore()

arial = font.load('Arial', 12, bold=True, italic=False)
text = 'Hello, world!'
glyphs = arial.get_glyphs(text)
glyph_string = GlyphString(text, glyphs)


#constants
grain = 16

#images / textures
textures = {}
for k,val in lookup.items():
	textures[k] = icons[val].get_texture()

cursor = icons['cursor']
cursortexture = cursor.get_texture()

#drawlists for cutting
cutList = {}
cutList[(0,1,0)] = YPOS
cutList[(0,-1,0)] = YNEG
cutList[(1,0,0)] = XPOS
cutList[(-1,0,0)] = XNEG
cutList[(0,0,1)] = ZPOS
cutList[(0,0,-1)] = ZNEG

#player globals
playerpos = Vec3(0,0,-5)
playervel = Vec3(0,0,0)
playercontrol = Vec3(0,0,0)
playeraim = Vec3(0,0,1)
playerflataim = Vec3(0,0,1)
playerflatside = Vec3(1,0,0)
playeraimyaw = 0
playeraimpitch = 0
aimpair = ((0,0,0),(0,1,0))

#x = 0
#d = 1
#t = 1

acceleration = 0.01

space = {}
plonk = 1
space[(0,0,0)] = plonk

def updateFromNetwork():
	global space
	mess = c.recvall()
	while len( mess ) > 0:
		m = mess[0]
		mess = mess[1:]
		print m
		if m[0]=='d':
			try:
				print "delete"
				pos = m[1:].split(',')
				print "from"
				pos = (int(pos[0]),int(pos[1]),int(pos[2]))
				print pos
				if pos in space:
					print "was there, deleted it"
					del space[pos]
					updateWorldList(pos)
			except:
				pass
		if m[0]=='a':
			try:
				print "add"
				pos = m[1:].split(',')
				print "to"
				mat = int(pos[0])
				print "a ",mat
				pos = (int(pos[1]),int(pos[2]),int(pos[3]))
				print "at ",pos
				if not pos in space:
					print "where is was empty"
					space[pos] = mat
					updateWorldList(pos)
			except:
				pass

edge = 8
genchunks = [ (0,0,0) ]
donechunks = []
def getNewChunks( start, excluding ):
	x,y,z = start
	potential = [(x+1,y,z),(x-1,y,z),
		(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)]
	actual = []
	for p in potential:
		if not p in excluding:
			actual.append(p)
	return actual
	
def density( x, y, z ):
	return 2*perlin3d(x,y,z,5,1,'') - y*8

def findGoodChunk(chunks):
	for chunk in chunks:
		disp = getDisplacementFromCube( chunk, (playerpos*(1.0/edge)).toTuple() )
		diff = abs(T2V(disp))
		if diff < 10.0/edge:
			chunks.remove(chunk)
			return chunk,chunks
	return None,chunks

def updateProcGen():
	global genchunks, space
	#print "updateProcGen"
	chunkToDo,genchunks = findGoodChunk(genchunks)
	if chunkToDo:
		#print chunkToDo
		start = tuple( x*edge for x in chunkToDo)
		#print start
		genlist = []
		for x in range(edge):
			for y in range(edge):
				for z in range(edge):
					genlist.append((x+start[0],y+start[1],z+start[2]))
		#print genlist
		filled = True
		for g in genlist:
			val = generateworld(g,'w')
			#h = density(g[0],g[1],g[2])
			#if h > 0:
			if val:
				space[g] = reverselookup[val]
				filled = True
		donechunks.append(chunkToDo)
		if filled:
			updateWorldList(genlist[0])
			newchunks = getNewChunks(chunkToDo,genchunks+donechunks)
			genchunks = genchunks + newchunks
	

def update(dt):
	global playerpos, playervel, aimpair, playeraim, playerflataim, playerflatside

	#update camera aim
	sy,cy = sin(playeraimyaw),cos(playeraimyaw)
	sp,cp = sin(playeraimpitch),cos(playeraimpitch)
	playeraim = Vec3( cp * sy, sp, cp * cy )
	playerflataim = Vec3( sy, 0, cy )
	playerflatside = playerflataim.crossY()

	#update physics
	realforward = playerflataim * playercontrol.z
	realside = playerflatside * playercontrol.x
	realcontrol = realforward + realside
	realcontrol.y = playercontrol.y
	diff = realcontrol - playervel
	acc = acceleration
	if playervel.dot( realcontrol ) < 0:
		acc = acc * 2
	diff.clampmag(acc)
	playervel = playervel + diff
	playerpos = playerpos + playervel
	aimpair = findIntersectingBlockAndVacancy()
	updateFromNetwork()
	#updateProcGen()

drawable = {}


def findIntersectingBlockAndVacancy():
	#return None
	best = None
	bestTime = 100
	genlist = []
	for cube,val in space.items():
		#for cube in genlist:
		test = intersects( cube, playerpos, playeraim )
		if test:
			time,diff = test
			if best and bestTime > time:
				best = None
			if not best:
				dest = (cube[0]+diff[0],cube[1]+diff[1],cube[2]+diff[2])
				best = (cube,dest)
				bestTime=time
	return best

#updateProcGen()
chunks = {}

def makeWorldList(x,y,z,dimension):
	listName = hash(repr((x,y,z)))
	#print (x,y,z)
	#print listName
	WATER = reverselookup['water']
	low = Vec3(x,y,z)*grain
	hi = Vec3(x+1,y+1,z+1)*grain
	glNewList(listName,GL_COMPILE)
	for loc, element in space.items():
		l = Vec3(loc[0],loc[1],loc[2])
		i,j,k = (l-low).toTuple()
		isWater = element == WATER
		if bounds( low, hi, l ):
			sides = []
			xpos = (loc[0]+1,loc[1]+0,loc[2]+0)
			ypos = (loc[0]+0,loc[1]+1,loc[2]+0)
			zpos = (loc[0]+0,loc[1]+0,loc[2]+1)
			xneg = (loc[0]-1,loc[1]-0,loc[2]-0)
			yneg = (loc[0]-0,loc[1]-1,loc[2]-0)
			zneg = (loc[0]-0,loc[1]-0,loc[2]-1)
			if isWater:
				if not xpos in space: sides.append( XPOS )
				if not xneg in space: sides.append( XNEG )
				if not ypos in space: sides.append( YPOS )
				if not yneg in space: sides.append( YNEG )
				if not zpos in space: sides.append( ZPOS )
				if not zneg in space: sides.append( ZNEG )
			else:
				if not xpos in space or space[xpos] == WATER: sides.append( XPOS )
				if not xneg in space or space[xneg] == WATER: sides.append( XNEG )
				if not ypos in space or space[ypos] == WATER: sides.append( YPOS )
				if not yneg in space or space[yneg] == WATER: sides.append( YNEG )
				if not zpos in space or space[zpos] == WATER: sides.append( ZPOS )
				if not zneg in space or space[zneg] == WATER: sides.append( ZNEG )
			
			if len(sides) > 0:
				glPushMatrix()
				glTranslatef(i,j,k)
				glScalef(0.5,0.5,0.5)
				texture = textures[element]
				glEnable(texture.target)
				glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
				glBindTexture(texture.target,texture.id)
				glBegin(GL_QUADS)
				for side in sides:
					draw_face(side)
				glEnd()
				glPopMatrix()
	glEndList()
	return listName
	
def updateWorldList(adjusted):
	global chunks
	x,y,z = adjusted
	x = x / grain
	y = y / grain
	z = z / grain
	chunks[(x,y,z)] = makeWorldList(x,y,z,grain)

pyglet.clock.schedule_interval(update, 0.016666)
rotScale = 0.0025


filename = "space.sav"

class LoadStruct:
	space = {}
	playerpos = Vec3(0,0,0)
	playeraimyaw = 0
	playeraimpitch = 0
	
def save():
	try:
		stuff = LoadStruct()
		stuff.space = space
		stuff.playerpos = playerpos
		stuff.playeraimyaw = playeraimyaw
		stuff.playeraimpitch = playeraimpitch
		f = open(filename,'wb')
		pickle.dump(stuff,f)
		f.close()
	except IOError:
		pass

try:
	f = open(filename,'rb')
	d = f.read()
	f.close()
	try:
		stuff = pickle.loads(d)
	except ImportError:
		stuff = pickle.loads(d.replace('\n','\r\n'))
	space = stuff.space
	if stuff.playerpos: playerpos = stuff.playerpos
	if stuff.playeraimyaw: playeraimyaw = stuff.playeraimyaw
	if stuff.playeraimpitch: playeraimpitch = stuff.playeraimpitch
	update(0)
except IOError:
	pass


# Direct OpenGL commands to this window.
window = pyglet.window.Window()
width,height = window.get_size()
print width, height
mode = 0
def switchMode(newMode):
	global mode,playercontrol
	mode = newMode
	if mode == 0:
		window.set_exclusive_mouse(True)
	else:
		window.set_exclusive_mouse(False)
		playercontrol = Vec3(0,0,0)
switchMode(mode)


todo = {}
#print len( space )
for k,v in space.items():
	t=(int(k[0]/16),int(k[1]/16),int(k[2]/16))
	todo[t] = True
#print len( todo )
for k,v in todo.items():
	#print k
	chunks[k] = makeWorldList(k[0],k[1],k[2],grain)
del todo

#chunks[(0,0,0)] = makeWorldList(0,0,0,grain)

@window.event
def on_mouse_motion(x, y, dx, dy):
	global playeraimyaw,playeraimpitch
	if mode == 0:
		playeraimyaw = playeraimyaw - dx * rotScale
		playeraimpitch = playeraimpitch + dy * rotScale

@window.event
def on_mouse_press(x,y, buttons, modifiers):
	global space
	if mode == 0:
		if aimpair:
			centre, vacancy = aimpair
			if buttons & mouse.LEFT:
				del space[centre]
				c.send("d"+str(centre[0])+','+str(centre[1])+','+str(centre[2]))
				updateWorldList(centre)
			if buttons & mouse.RIGHT:
				space[vacancy] = plonk
				c.send("a"+str(plonk)+','+str(vacancy[0])+','+str(vacancy[1])+','+str(vacancy[2]))
				updateWorldList(vacancy)

newRenderer = True
	
@window.event
def on_key_press(symbol, modifiers):
	global plonk,newRenderer
	if mode == 0:
		if symbol == key.A:
			playercontrol.x = 1
		if symbol == key.D:
			playercontrol.x = -1
		if symbol == key.W:
			playercontrol.z = 1
		if symbol == key.S:
			playercontrol.z = -1
		if symbol == key.SPACE:
			playercontrol.y = 1
		if symbol == key.LSHIFT:
			playercontrol.y = -1
		if symbol == key._1:
			plonk = 1
		if symbol == key._2:
			plonk = 2
		if symbol == key._3:
			plonk = 3
		if symbol == key.F1:
			newRenderer = not newRenderer
	if symbol == key.TAB:
		switchMode( 1 - mode )

@window.event
def on_key_release(symbol, modifiers):
	if mode == 0:
		if symbol == key.A or symbol == key.D:
			playercontrol.x = 0
		if symbol == key.W or symbol == key.S:
			playercontrol.z = 0
		if symbol == key.SPACE or symbol == key.LSHIFT:
			playercontrol.y = 0
			
@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
	global plonk
	plonk = plonk - scroll_y
	while plonk < 1:
		plonk = plonk + MAX_ID
	while plonk > MAX_ID:
		plonk = plonk - MAX_ID

@window.event
def on_draw():
	global t,shader

	glEnable(GL_DEPTH_TEST)
	#shader.bind()
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(70,width*1.0/height,0.01,1000)
	targetLook = playerpos + playeraim
	gluLookAt(playerpos.x,playerpos.y,playerpos.z, targetLook.x,targetLook.y,targetLook.z, 0,1,0)

	glClearColor(0.5, 0.8, 0.9, 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)

	# fallback

	glColor3f(1,1,1)

	glLoadIdentity()
	# the elements of space

	if newRenderer:
		for location, element in chunks.items():
			glPushMatrix()
			i,j,k = location[0],location[1],location[2]
			glTranslatef(i*grain,j*grain,k*grain)
			glCallList(element)
			glPopMatrix()
	else:
		for location, element in space.items():
			glPushMatrix()
			i,j,k = location[0],location[1],location[2]
			glTranslatef(i,j,k)
			glScalef(0.5,0.5,0.5)
			#glColor4f(1.0,0.0,1.0,1.0)
			texture = textures[element]
			glEnable(texture.target)
			glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
			glBindTexture(texture.target,texture.id)
			glCallList(CUBE)
			glPopMatrix()
	if aimpair:
		glPushMatrix()
		loc = aimpair[0]
		dest = aimpair[1]
		direc = ( dest[0]-loc[0], dest[1]-loc[1], dest[2]-loc[2] )
		i,j,k = loc[0],loc[1],loc[2]
		glTranslatef(i,j,k)
		glScalef(0.5,0.5,0.5)
		glColor4f(1.0,0.0,0.0,0.5)
		glCallList(cutList[direc])
		glPopMatrix()		

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	w = width / 2
	h = height / 2
	glOrtho(-w,w,-h,h,-1,1);
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glColor4f(1.0,1.0,1.0,0.9)
	glScalef(16.0,16.0,0.1)
	glEnable(cursortexture.target)
	glBindTexture(cursortexture.target,cursortexture.id)
	glCallList(ZNEG)

	glDisable(GL_DEPTH_TEST)
	glLoadIdentity()
	glTranslatef(8+16-w,8+16-h,0)
	glScalef(16.0,16.0,0.1)
	texture = textures[plonk]
	glEnable(texture.target)
	glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glBindTexture(texture.target,texture.id)
	glCallList(ZNEG)
	
	glLoadIdentity()
	glTranslatef(8+16+16+8-w,8+16-h,0)
	glPushMatrix()
	glColor4f(0,0,0,0.5)
	glyph_string.draw()
	glTranslatef(0,2,0)
	glyph_string.draw()
	glTranslatef(2,0,0)
	glyph_string.draw()
	glTranslatef(0,-2,0)
	glyph_string.draw()
	glPopMatrix()		
	glTranslatef(1,1,0)
	glColor4f(1.0,1.0,1.0,1.0)
	glyph_string.draw()

pyglet.app.run()
save()
