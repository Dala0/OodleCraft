from pyglet.gl import *
from pyglet import image
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

class playerStruct:
	pos = Vec3(0,0,0)
	pitch = 0
	yaw = 0
	
players = {}
import getpass
username = getpass.getuser()

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
		#print m
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
		if m[0]=='p':
			try:
				vals = m[1:].split(',')
				pos = Vec3(vals[0],vals[1],vals[2])
				pitch = vals[3]
				yaw = vals[4]
				name = vals[5]
				player = playerStruct()
				player.pos = pos
				player.pitch = pitch
				player.yaw = yaw
				players[name] = player
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

def netpush(dt):
	c.send("p"+str(playerpos.x)+','+str(playerpos.y)+','+str(playerpos.z)+','+str(playeraimpitch)+','+str(playeraimyaw)+','+str(username))
				
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

def tadd(a,b):
	return tuple(map(lambda t: t[0]+t[1],zip(a,b)))
def tsub(a,b):
	return tuple(map(lambda t: t[0]-t[1],zip(a,b)))
def tdiv(a,b):
	return tuple(map(lambda t: t[0]/t[1],zip(a,b)))
def tmul(a,b):
	return tuple(map(lambda t: t[0]*t[1],zip(a,b)))

def findIntersectingBlockAndVacancy():
	#return None
	start = (playerpos+Vec3(0.5,0.5,0.5)).toTuple()
	startcell = (int(start[0]),int(start[1]),int(start[2]))
	startcell = tuple(map(lambda t: int([t,t-1][t<0]), start))

	direc = playeraim.toTuple()
	current = tsub( start, startcell )
	current = tuple(map(lambda t: [1-t[0],t[0]][t[1]<0], zip(current,direc)))
	move = tuple(map(lambda t: [1,-1][t<0], direc))
	advance = tuple(map(lambda t: [t,-t][t<0], direc))
	times = tuple(map(lambda t: t[0]/[t[1],0.0001][t[1]==0], zip(current,advance)))
	
	currentcell = startcell
	
	time = 0
	while time < 10:
		amount = times[2]
		choice = (0,0,move[2])
		if times[0] < times[1] and times[0] < times[2]:
			amount = times[0]
			choice = (move[0],0,0)
		elif times[1] < times[2]:
			amount = times[1]
			choice = (0,move[1],0)
		amount = amount + 0.001
		current = tuple(map(lambda t: t[0]-t[1]*amount, zip(current,advance)))
		current = tuple(map(lambda t: [t,t+1][t<=0], current))
		nextcell = tadd( currentcell,choice )
		if nextcell in space:
			return nextcell, currentcell
		currentcell = nextcell
		time = time + amount
		times = tuple(map(lambda t: t[0]/[t[1],0.0001][t[1]==0], zip(current,advance)))
	return None

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
pyglet.clock.schedule_interval(netpush, 0.1)

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
window.set_exclusive_mouse(True)
def switchMode():
	global mode,playercontrol
	mode = 1-mode
	if mode == 0:
		window.set_exclusive_mouse(True)
	else:
		window.set_exclusive_mouse(False)
		playercontrol = Vec3(0,0,0)


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

def changeMaterial( inc ):
	global plonk
	plonk = plonk - inc
	while plonk < 1:
		plonk = plonk + MAX_ID
	while plonk > MAX_ID:
		plonk = plonk - MAX_ID

def changeaim( yaw, pitch ):
	global playeraimyaw, playeraimpitch
	playeraimyaw = playeraimyaw + yaw
	playeraimpitch = playeraimpitch + pitch
	print playeraimyaw
	PI = 3.141
	if playeraimpitch < -PI/2:
		playeraimpitch = -PI/2
	if playeraimpitch > PI/2:
		playeraimpitch = PI/2
	if playeraimyaw < -PI:
		playeraimyaw = playeraimyaw + PI*2
	if playeraimyaw > PI:
		playeraimyaw = playeraimyaw - PI*2
		

@window.event
def on_mouse_motion(x, y, dx, dy):
	game_on_mouse_motion(globals(), x, y, dx, dy )

@window.event
def on_mouse_drag(x, y, dx, dy):
	game_on_mouse_motion(globals(), x, y, dx, dy )

@window.event
def on_mouse_press(x,y, buttons, modifiers):
	game_on_mouse_press(globals(), x, y, buttons, modifiers)

from controls import *
	
@window.event
def on_key_press(symbol, modifiers):
	game_on_key_press(globals(),symbol, modifiers)

@window.event
def on_key_release(symbol, modifiers):
	game_on_key_release(globals(),symbol, modifiers)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
	game_on_mouse_scroll(globals(),x, y, scroll_x, scroll_y)

from drawing import *
	
@window.event
def on_draw():
	game_on_draw(globals())

pyglet.app.run()
save()
