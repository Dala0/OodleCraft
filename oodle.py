#!/usr/bin/python
from pyglet.gl import *
from pyglet import image
from pyglet import font
from pyglet.font import GlyphString
import struct

from math import * # trigonometry
from vec import *
from geom import *
import pickle
import glPrims
from assets import *
import materials
from worldgen import *
from time import time

class GameState(dict):
	def __init__(self, *args):
		dict.__init__(self, args)
		dict.__setitem__(self, "timeout", 2 )
		dict.__setitem__(self, "newarrival", False )

	# these functions let state-functions access items as if they were elements
	def __getattr__(self, attr):
		val = dict.__getitem__(self, attr)
		return val
	def __setattr__(self, attr, value):
		dict.__setitem__(self, attr, value)
        
state = GameState()
glPrims.filloutPrims( state )
materials.addmaterials( state )

#import procgen
#procgen.addprocgentostate( state )

import netcore

state.c = netcore.netcore()

class playerStruct:
	pos2 = Vec3(0,1,0)
	vel2 = Vec3(0,1,0)
	pos = Vec3(0,1,0)
	vel = Vec3(0,1,0)
	pitch = 0
	yaw = 0
	
state.players = {}
import getpass
state.username = getpass.getuser()

arial = font.load('Arial', 12, bold=True, italic=False)
text = 'Hello, world!'
glyphs = arial.get_glyphs(text)
state.glyph_string = GlyphString(text, glyphs)


#constants
state.grain = 16

#images / textures
state.textures = {}
for k,val in materials.lookup.items():
	state.textures[k] = icons[val].get_texture()

cursor = icons['cursor']
state.cursortexture = cursor.get_texture()

#drawlists for cutting
cutList = {}
cutList[(0,1,0)] = glPrims.YPOS
cutList[(0,-1,0)] = glPrims.YNEG
cutList[(1,0,0)] = glPrims.XPOS
cutList[(-1,0,0)] = glPrims.XNEG
cutList[(0,0,1)] = glPrims.ZPOS
cutList[(0,0,-1)] = glPrims.ZNEG
state.cutList = cutList

#player globals
state.playerpos = Vec3(0,0,-5)
state.playervel = Vec3(0,0,0)
state.playercontrol = Vec3(0,0,0)
state.flying = True
state.playeraim = Vec3(0,0,1)
state.playerflataim = Vec3(0,0,1)
state.playerflatside = Vec3(1,0,0)
state.playeraimyaw = 0
state.playeraimpitch = 0
state.playerradius = 0.4
state.aimpair = ((0,0,0),(0,1,0))

#x = 0
#d = 1
#t = 1

acceleration = 0.01

state.space = {}
state.plonk = 1
state.space[(0,0,0)] = state.plonk

def updateFromNetwork(s):
	for peer in s.c.peers:	
		mess = peer.urecvall()
		while len( mess ) > 0:
			m = mess[0]
			mess = mess[1:]
			#if not m[0]=='p':
			#	print m
			if m[0]=='d':
				try:
					#print "delete"
					pos = m[1:].split(',')
					#print "from"
					pos = (int(pos[0]),int(pos[1]),int(pos[2]))
					#print pos
					if pos in s.space:
						#print "was there, deleted it"
						del s.space[pos]
						s.updateWorldList(s,pos)
				except:
					pass
			if m[0]=='a':
				try:
					#print "add"
					pos = m[1:].split(',')
					#print "to"
					mat = int(pos[0])
					#print "a ",mat
					pos = (int(pos[1]),int(pos[2]),int(pos[3]))
					#print "at ",pos
					if not pos in s.space:
						#print "where is was empty"
						s.space[pos] = mat
						s.updateWorldList(s,pos)
				except:
					pass
			#if m[0]=='i': # informed by other player
			#	try:
			#		#print "i",
			#		pos = m[1:].split(',')
			#		mat = int(pos[0])
			#		pos = (int(pos[1]),int(pos[2]),int(pos[3]))
			#		s.space[pos] = mat
			#		s.updateWorldList(s,pos)
			#	except:
			#		pass
			#if m[0]=='f': # finished inform by other player
			#	try:
			#		print "received data and updating"
			#		s.updateFromAllSpace(s)
			#	except:
			#		pass
			if m[0]=='p':
				try:
					#print "person"
					vals = m[1:].split(',')
					pos = Vec3(vals[0],vals[1],vals[2])
					#print "@",pos
					pitch = vals[3]
					yaw = vals[4]
					#print "pitch:",pitch," yaw:",yaw
					name = vals[5]
					#print "called:",name
					player = playerStruct()
					player.pos = pos
					player.pitch = pitch
					player.yaw = yaw
					player.lastSeen = time()
					if not name in s.players:
						s.newarrival = True
						print "new arrival : ",name
						peer.name = name
					s.players[name] = player
				except:
					pass
	#if s.newarrival:
	#	print "sending my data"
	#	for key, value in s.space.items():
	#		s.c.send("i"+str(value)+','+str(key[0])+','+str(key[1])+','+str(key[2]))
	#	s.c.send("f")
	#	s.newarrival = False
		

def netpush(dt):
	state.c.send("p"+str(state.playerpos.x)+','+str(state.playerpos.y)+','+str(state.playerpos.z)+','+str(state.playeraimpitch)+','+str(state.playeraimyaw)+','+str(state.username))
				
def collisionAndResponse():
	pp = state.playerpos
	lx = int(pp.x)
	ly = int(pp.y)
	lz = int(pp.z)
	if pp.x < 0:
		lx = lx - 1
	if pp.y < 0:
		ly = ly - 1
	if pp.z < 0:
		lz = lz - 1
	dx = pp.x - lx
	dy = pp.y - ly
	dz = pp.z - lz
	#do floor
	se = (lx,ly-1,lz) in state.space
	sw = (lx+1,ly-1,lz) in state.space
	ne = (lx,ly-1,lz+1) in state.space
	nw = (lx+1,ly-1,lz+1) in state.space
	overlap = 0.5 - state.playerradius 
	underlap = 1.0 - overlap
	if dx > underlap:
		sw = False
		nw = False
	if dx < overlap:
		se = False
		ne = False
	if dz > underlap:
		se = False
		sw = False
	if dz < overlap:
		ne = False
		nw = False
	infloor = sw or se or nw or ne
	if infloor and dy < 0.5:
		state.playerpos.y = ly + 0.5
		dy = pp.y - ly
		state.playervel.y = max( state.playervel.y, 0 )
	if infloor and not state.flying and state.playercontrol.y > 0.5:
		state.playervel.y = 0.2
	#do sides
	se = (lx,ly,lz) in state.space or (lx,ly+1,lz) in state.space 
	sw = (lx+1,ly,lz) in state.space or (lx+1,ly+1,lz) in state.space 
	ne = (lx,ly,lz+1) in state.space or (lx,ly+1,lz+1) in state.space 
	nw = (lx+1,ly,lz+1) in state.space or (lx+1,ly+1,lz+1) in state.space 
	#print "lx,lz : ",lx,':',dx,',',lz,':',dz," ",nw,ne,sw,se
	if dx > overlap:
		if ( nw and dz > 0.5 ) or ( sw and dz < 0.5 ):
			state.playerpos.x = lx + overlap
			dx = pp.x - lx
			state.playervel.x = 0
	if dx < underlap:
		if ( ne and dz > 0.5 ) or ( se and dz < 0.5 ):
			state.playerpos.x = lx + underlap
			dx = pp.x - lx
			state.playervel.x = 0
	if dz > overlap:
		if ( nw and dx > 0.5 ) or ( ne and dx < 0.5 ):
			state.playerpos.z = lz + overlap
			dz = pp.z - lz
			state.playervel.z = 0
	if dz < underlap:
		if ( sw and dx > 0.5 ) or ( se and dx < 0.5 ):
			state.playerpos.z = lz + underlap
			dz = pp.z - lz
			state.playervel.z = 0
				
def update(dt):
	#update camera aim
	sy,cy = sin(state.playeraimyaw),cos(state.playeraimyaw)
	sp,cp = sin(state.playeraimpitch),cos(state.playeraimpitch)
	state.playeraim = Vec3( cp * sy, sp, cp * cy )
	state.playerflataim = Vec3( sy, 0, cy )
	state.playerflatside = state.playerflataim.crossY()

	#update physics
	realforward = state.playerflataim * state.playercontrol.z
	realside = state.playerflatside * state.playercontrol.x
	realcontrol = realforward + realside
	realcontrol.y = state.playercontrol.y
	diff = realcontrol - state.playervel
	if not state.flying:
		diff.y = 0
	acc = acceleration
	if state.playervel.dot( realcontrol ) < 0:
		acc = acc * 2
	diff.clampmag(acc)
	if not state.flying:
		diff.y = diff.y - dt * 0.7
	state.playervel = state.playervel + diff
	state.playerpos = state.playerpos + state.playervel
	collisionAndResponse()
	state.aimpair = findIntersectingBlockAndVacancy()
	updateFromNetwork(state)
	#updateProcGen()
	currentTime = time()
	removables = {}
	newdic = {}
	for key, value in state.players.items():
		if value.lastSeen+state.timeout > currentTime:
			newdic[ key ] = value
		else:
			removables[ key ] = value
	for key, value in removables.items():
		print "TIMING OUT : ",key
	state.players = newdic

state.drawable = {}

def tadd(a,b):
	return tuple(map(lambda t: t[0]+t[1],zip(a,b)))
def tsub(a,b):
	return tuple(map(lambda t: t[0]-t[1],zip(a,b)))
def tdiv(a,b):
	return tuple(map(lambda t: t[0]/t[1],zip(a,b)))
def tmul(a,b):
	return tuple(map(lambda t: t[0]*t[1],zip(a,b)))

def findIntersectingBlockAndVacancy():
	# offset by 0.5 for the grid, then one in Y for the height of the player
	start = (state.playerpos+Vec3(0.5,1.5,0.5)).toTuple()
	# map to the base grid positions (-0.5 --> -1)
	startcell = tuple(map(lambda t: int([t,t-1][t<0]), start))

	# get the direction of the ray cast
	direc = state.playeraim.toTuple()
	# get the current distance to go in each axis
	current = tsub( start, startcell )
	current = tuple(map(lambda t: [1-t[0],t[0]][t[1]<0], zip(current,direc)))
	# make the move direction per axis
	move = tuple(map(lambda t: [1,-1][t<0], direc))
	# make the amount moved in current when moving with time
	advance = tuple(map(lambda t: [t,-t][t<0], direc))
	# make the "how long until we cross a boundary" per axis
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
		if nextcell in state.space:
			return nextcell, currentcell
		currentcell = nextcell
		time = time + amount
		times = tuple(map(lambda t: t[0]/[t[1],0.0001][t[1]==0], zip(current,advance)))
	return None

#updateProcGen()
state.chunks = {}

def makeWorldList(state,x,y,z):
	listName = hash(repr((x,y,z)))
	#print (x,y,z)
	#print listName
	WATER = state.reverselookup['water']
	low = Vec3(x,y,z)*state.grain
	hi = Vec3(x+1,y+1,z+1)*state.grain
	glNewList(listName,GL_COMPILE)
	for loc, element in state.space.items():
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
				if not xpos in state.space: sides.append( XPOS )
				if not xneg in state.space: sides.append( XNEG )
				if not ypos in state.space: sides.append( YPOS )
				if not yneg in state.space: sides.append( YNEG )
				if not zpos in state.space: sides.append( ZPOS )
				if not zneg in state.space: sides.append( ZNEG )
			else:
				if not xpos in state.space or state.space[xpos] == WATER: sides.append( state.XPOS )
				if not xneg in state.space or state.space[xneg] == WATER: sides.append( state.XNEG )
				if not ypos in state.space or state.space[ypos] == WATER: sides.append( state.YPOS )
				if not yneg in state.space or state.space[yneg] == WATER: sides.append( state.YNEG )
				if not zpos in state.space or state.space[zpos] == WATER: sides.append( state.ZPOS )
				if not zneg in state.space or state.space[zneg] == WATER: sides.append( state.ZNEG )
			
			if len(sides) > 0:
				glPushMatrix()
				glTranslatef(i,j,k)
				glScalef(0.5,0.5,0.5)
				texture = state.textures[element]
				glEnable(texture.target)
				glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
				glBindTexture(texture.target,texture.id)
				glBegin(GL_QUADS)
				for side in sides:
					state.draw_face(side)
				glEnd()
				glPopMatrix()
	glEndList()
	return listName
state.makeWorldList = makeWorldList
	
def updateWorldList(state,adjusted):
	#global chunks
	x,y,z = adjusted
	potential = []
	for X in range(x-1,x+2):
		for Y in range( y-1, y+2 ):
			for Z in range( z-1, z+2):
				potential.append((X,Y,Z))
	state.refreshFor( state, potential )
state.updateWorldList = updateWorldList

pyglet.clock.schedule_interval(update, 0.016666)
pyglet.clock.schedule_interval(netpush, 0.1)

filename = state.username+".sav"

class LoadStruct:
	space = {}
	playerpos = Vec3(0,0,0)
	playeraimyaw = 0
	playeraimpitch = 0
	
def save():
	try:
		stuff = LoadStruct()
		stuff.space = state.space
		stuff.playerpos = state.playerpos
		stuff.playeraimyaw = state.playeraimyaw
		stuff.playeraimpitch = state.playeraimpitch
		f = open(filename,'wb')
		pickle.dump(stuff,f)
		f.close()
		f = open('bin'+filename,'wb')
		f.write( struct.pack( "fffff",state.playerpos.x,state.playerpos.y,state.playerpos.z,state.playeraimyaw,state.playeraimpitch) )
		f.write( struct.pack( "i", len(state.space.keys() ) ) )
		for key, value in state.space.items():
			f.write( struct.pack( "iiii",key[0],key[1],key[2],value) )
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
	state.space = stuff.space
	if stuff.playerpos: state.playerpos = stuff.playerpos
	if stuff.playeraimyaw: state.playeraimyaw = stuff.playeraimyaw
	if stuff.playeraimpitch: state.playeraimpitch = stuff.playeraimpitch
	update(0)
except IOError:
	pass


# Direct OpenGL commands to this window.
window = pyglet.window.Window()
state.width,state.height = window.get_size()
#print state.width, state.height
state.mode = 0
window.set_exclusive_mouse(True)
def switchMode(state):
	state.mode = 1-state.mode
	if state.mode == 0:
		window.set_exclusive_mouse(True)
	else:
		window.set_exclusive_mouse(False)
		state.playercontrol = Vec3(0,0,0)
state.switchMode = switchMode

def refreshFor( state, cells ):
	todo = {}
	#print len( space )
	for k in cells:
		t=(int(k[0]/state.grain),int(k[1]/state.grain),int(k[2]/state.grain))
		todo[t] = True
	#print len( todo )
	for k in todo.keys():
		#print k
		state.chunks[k] = state.makeWorldList(state,k[0],k[1],k[2])
state.refreshFor = refreshFor
refreshFor( state, state.space.keys() )

def updateFromAllSpace(state):
	state.refreshFor(state, state.space.keys())
state.updateFromAllSpace = updateFromAllSpace

#chunks[(0,0,0)] = makeWorldList(0,0,0,grain)

def changeMaterial( state, inc ):
	state.plonk = state.plonk - inc
	while state.plonk < 1:
		state.plonk = state.plonk + state.MAX_ID
	while state.plonk > state.MAX_ID:
		state.plonk = state.plonk - state.MAX_ID
state.changeMaterial = changeMaterial

def changeaim( state, yaw, pitch ):
	state.playeraimyaw = state.playeraimyaw + yaw
	state.playeraimpitch = state.playeraimpitch + pitch
	PI = 3.141
	if state.playeraimpitch < -PI/2:
		state.playeraimpitch = -PI/2
	if state.playeraimpitch > PI/2:
		state.playeraimpitch = PI/2
	if state.playeraimyaw < -PI:
		state.playeraimyaw = state.playeraimyaw + PI*2
	if state.playeraimyaw > PI:
		state.playeraimyaw = state.playeraimyaw - PI*2
state.changeaim = changeaim

@window.event
def on_mouse_motion(x, y, dx, dy):
	game_on_mouse_motion(state, x, y, dx, dy )

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	game_on_mouse_motion(state, x, y, dx, dy )

@window.event
def on_mouse_press(x,y, buttons, modifiers):
	game_on_mouse_press(state, x, y, buttons, modifiers)

from controls import *
	
@window.event
def on_key_press(symbol, modifiers):
	game_on_key_press(state,symbol, modifiers)

@window.event
def on_key_release(symbol, modifiers):
	game_on_key_release(state,symbol, modifiers)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
	game_on_mouse_scroll(state,x, y, scroll_x, scroll_y)

from drawing import *
	
@window.event
def on_draw():
	game_on_draw(state)

pyglet.app.run()
save()
