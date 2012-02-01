from pyglet.gl import *
from pyglet import image
from pyglet.window import key
from pyglet.window import mouse
from math import * # trigonometry
from vec import *
from geom import *
import pickle
from glPrims import *
from assets import *
from materials import *

import threading
import netcore
import time
c = netcore.netcore()
mess = []
def readMessages():
	global c
	while c:
		ms = c.recvall()
		for m in ms:
			mess.append( m )
		time.sleep(0.1)
def sendMessage(message):
	global c
	c.sendable.append(message)
t = threading.Thread(target=readMessages)
t.daemon = True
t.start()

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

def update(dt):
	global playerpos, playervel, aimpair, playeraim, playerflataim, playerflatside, space

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
	for m in mess:
		if m[0]=='d':
			try:
				pos = m[1:].split(',')
				pos = Vec3(int(pos[0]),int(pos[1]),int(pos[2]))
				pos = pos.toTuple()
				if pos in space:
					del space[pos]
			except:
				pass
		if m[0]=='a':
			try:
				pos = m[1:].split(',')
				mat = int(pos[0])
				pos = Vec3(int(pos[1]),int(pos[2]),int(pos[3]))
				pos = pos.toTuple()
				if not pos in space:
					space[pos] = mat
			except:
				pass

drawable = {}


def findIntersectingBlockAndVacancy():
	best = None
	bestTime = 100
	for cube,val in space.items():
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

chunks = {}

def makeWorldList(x,y,z,dimension):
	listName = hash(repr((x,y,z)))
	#print (x,y,z)
	#print listName
	low = Vec3(x,y,z)*grain
	hi = Vec3(x+1,y+1,z+1)*grain
	glNewList(listName,GL_COMPILE)
	for location, element in space.items():
		l = Vec3(location[0],location[1],location[2])
		i,j,k = (l-low).toTuple()
		if bounds( low, hi, l ):
			glPushMatrix()
			glTranslatef(i,j,k)
			glScalef(0.5,0.5,0.5)
			texture = textures[element]
			glEnable(texture.target)
			glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
			glBindTexture(texture.target,texture.id)
			glBegin(GL_QUADS)
			draw_cube()
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
				sendMessage("d"+str(centre[0])+','+str(centre[1])+','+str(centre[2]))
				updateWorldList(centre)
			if buttons & mouse.RIGHT:
				space[vacancy] = plonk
				sendMessage("a"+str(plonk)+','+str(centre[0])+','+str(centre[1])+','+str(centre[2]))
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
	gluPerspective(90,1,0.01,1000)
	targetLook = playerpos + playeraim
	gluLookAt(playerpos.x,playerpos.y,playerpos.z, targetLook.x,targetLook.y,targetLook.z, 0,1,0)

	glClearColor(0.0, 0.0, 0.0, 1.0)
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

	glLoadIdentity()
	glTranslatef(8+16-w,8+16-h,0)
	glScalef(16.0,16.0,0.1)
	texture = textures[plonk]
	glEnable(texture.target)
	glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glBindTexture(texture.target,texture.id)
	glCallList(ZNEG)
pyglet.app.run()
save()
