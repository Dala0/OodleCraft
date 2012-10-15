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

class WorldState(dict):
	def __init__(self, *args):
		dict.__init__(self, args)

	# these functions let world-functions access items as if they were elements
	def __getattr__(self, attr):
		val = dict.__getitem__(self, attr)
		return val
	def __setattr__(self, attr, value):
		dict.__setitem__(self, attr, value)
        
state = GameState()
glPrims.filloutPrims( state )
materials.addmaterials( state )

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

arial = font.load('Arial', 10, bold=True, italic=False)
glyphs = None
def SetMessage( s, message ):
	glyphs = arial.get_glyphs(message)
	s.glyph_string = GlyphString(message, glyphs)
SetMessage(state, "Tab to switch mode, ESC for menu")
state.SetMessage = SetMessage
state.debuglog = []
state.debuglimit = 25
courier = font.load('Courier', 8, bold=True, italic=False)
def DebugLog( s, message ):
	return
	glyphs = courier.get_glyphs(message)
	s.debuglog.append( (message,GlyphString(message,glyphs)) )
	if len( s.debuglog ) > s.debuglimit:
		s.debuglog = s.debuglog[-s.debuglimit:]
state.DebugLog = lambda m : DebugLog(state, m )

#constants
state.grain = 16
state.invwcount = 8
state.invx = 16
state.invy = 16
state.invs = 32
state.invb = 8

#images / textures
state.textures = {}
for k,val in materials.lookup.items():
	state.textures[k] = icons[val].get_texture()

cursor = icons['cursor']
state.cursortexture = cursor.get_texture()

#drawlists for cutting
cutList = {}
cutList[(0,1,0)] = glPrims.draw_YPOS
cutList[(0,-1,0)] = glPrims.draw_YNEG
cutList[(1,0,0)] = glPrims.draw_XPOS
cutList[(-1,0,0)] = glPrims.draw_XNEG
cutList[(0,0,1)] = glPrims.draw_ZPOS
cutList[(0,0,-1)] = glPrims.draw_ZNEG
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
state.aimpair = ((0,0,0),(0,1,0),0,0) # aimpair also includes the world and the distance
state.mouse_action_start = None
state.inDelete = False
state.inInsert = False
state.hasMovedSinceStartedClicking = False
state.headoffset = Vec3(0.5,1.5,0.5)

state.mode = 0
state.MODE_EDIT = 0
state.MODE_PAINTING = 1
state.MODE_DRIVING = 2
state.MODE_MAX_MODE = 3
def switchMode(state):
	state.mode = (1+state.mode)%state.MODE_MAX_MODE
	if state.mode == state.MODE_EDIT:
		state.SetMessage(state,"Editing Mode")
	elif state.mode == state.MODE_PAINTING:
		state.SetMessage(state,"Painting Mode")
	elif state.mode == state.MODE_DRIVING:
		state.SetMessage(state,"Driving Mode")
state.switchMode = lambda : switchMode( state )

maxvelocity = 0.3
acceleration = 0.02

state.worlds = [ WorldState() ];
state.worlds[0].space = {}
state.worlds[0].index = 0
state.currentWorld = state.worlds[0]
state.currentWorld.chunks = {}
state.currentWorld.pos = Vec3(0,0,0)
state.currentWorld.yaw = 0
state.plonk = 1
state.brushsize = 1
state.worlds[0].space[(0,0,0)] = state.plonk

def SeedLand(s):
	w = WorldState()
	w.index = len(s.worlds)
	w.space = {}
	w.space[(0,0,0)] = state.plonk
	w.chunks = {}
	w.pos = s.playerpos
	w.yaw = s.playeraimyaw
	s.worlds.append( w )
	s.updateWorldList(w,(0,0,0))
	s.c.send("wa"+str(w.index)+','+str(w.pos.x)+','+str(w.pos.y)+','+str(w.pos.z)+','+str(w.yaw)+','+str(state.plonk))
state.SeedLand = lambda : SeedLand(state)
	

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
					if pos in s.worlds[0].space:
						#print "was there, deleted it"
						del s.currentWorld.space[pos]
						s.updateWorldList(s.currentWorld,pos)
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
					if not pos in s.worlds[0].space:
						#print "where is was empty"
						s.currentWorld.space[pos] = mat
						s.updateWorldList(s.currentWorld,pos)
				except:
					pass
			#if m[0]=='i': # informed by other player
			#	try:
			#		#print "i",
			#		pos = m[1:].split(',')
			#		mat = int(pos[0])
			#		pos = (int(pos[1]),int(pos[2]),int(pos[3]))
			#		s.orlds[0].space[pos] = mat
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
	#	for key, value in s.worlds[0].space.items():
	#		s.c.send("i"+str(value)+','+str(key[0])+','+str(key[1])+','+str(key[2]))
	#	s.c.send("f")
	#	s.newarrival = False
		

def netpush(dt):
	state.c.send("p"+str(state.playerpos.x)+','+str(state.playerpos.y)+','+str(state.playerpos.z)+','+str(state.playeraimpitch)+','+str(state.playeraimyaw)+','+str(state.username))
				
def collidable(state, world, point):
	return point in world.space and world.space[point] != state.reverselookup['water']
def collisionAndResponse(world):
	# change to a cube collision (it's currently trying to be a cylinder collision really badly)
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
	coll = lambda pos : collidable(state,world,pos)
	se = coll((lx,ly-1,lz))
	sw = coll((lx+1,ly-1,lz))
	ne = coll((lx,ly-1,lz+1))
	nw = coll((lx+1,ly-1,lz+1))
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
	se = coll((lx,ly,lz)) or coll((lx,ly+1,lz))
	sw = coll((lx+1,ly,lz)) or coll((lx+1,ly+1,lz))
	ne = coll((lx,ly,lz+1)) or coll((lx,ly+1,lz+1))
	nw = coll((lx+1,ly,lz+1)) or coll((lx+1,ly+1,lz+1))
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
	realcontrol.clampmag(maxvelocity)
	diff = realcontrol - state.playervel
	if not state.flying:
		diff.y = 0
	diff.clampmag(acceleration)
	if not state.flying:
		diff.y = diff.y - dt * 0.7
	state.playervel = state.playervel + diff
	oldPlayerPos = state.playerpos
	state.playerpos = state.playerpos + state.playervel
	collisionAndResponse(state.worlds[0])
	playerMotion = state.playerpos - oldPlayerPos
	if state.mode == state.MODE_DRIVING: # driving mode
		if state.currentWorld != state.worlds[0]:
			state.currentWorld.pos = state.currentWorld.pos + playerMotion
	state.aimpair = findIntersectingBlockAndVacancy(state)
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

def localFromWorld(w, start, aim):
	wl = start-w.pos
	s = sin(w.yaw)
	c = cos(w.yaw)
	localStart = Vec3( c * wl.x - s * wl.z, wl.y, wl.z * c + s * wl.x )
	localAim = Vec3( c * aim.x - s * aim.z, aim.y, aim.z * c + s * aim.x )
	return (localStart,localAim)

def findIntersectingBlockAndVacancy(state):
	best = None
	besttime = 10

	for world in state.worlds:
		# offset by 0.5 for the grid, then one in Y for the height of the player
		worldlocal,worldaim = localFromWorld(world,state.playerpos,state.playeraim)
		#wl = state.playerpos-world.pos
		#s = sin(world.yaw)
		#c = cos(world.yaw)
		#worldlocal = Vec3( c * wl.x - s * wl.z, wl.y, wl.z * c + s * wl.x )
		start = (worldlocal+state.headoffset).toTuple()
		# map to the base grid positions (-0.5 --> -1)
		startcell = tuple(map(lambda t: int([t,t-1][t<0]), start))

		# get the direction of the ray cast
		#wa = state.playeraim
		#worldaim = Vec3( c * wa.x - s * wa.z, wa.y, wa.z * c + s * wa.x )
		direc = worldaim.toTuple()
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
		while time < besttime:
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
			if nextcell in world.space:
				best = (nextcell, currentcell, world.index,time)
				besttime = time
				continue
			currentcell = nextcell
			time = time + amount
			times = tuple(map(lambda t: t[0]/[t[1],0.0001][t[1]==0], zip(current,advance)))
	return best

def getInAirPoint(state):
	world = state.worlds[state.mouse_action_start[2]]
	worldlocal,worldaim = localFromWorld(world,state.playerpos,state.playeraim)
	start = ( state.headoffset+worldlocal + worldaim * state.mouse_action_start[3] ).toTuple()
	startcell = tuple(map(lambda t: int([t,t-1][t<0]), start))
	return map(int,startcell)
state.getInAirPoint = lambda : getInAirPoint(state)
#updateProcGen()

def vrange( low, high ):
	for x in xrange( int(low[0]), int(high[0]) ):
		for y in xrange( int(low[1]), int(high[1]) ):
			for z in xrange( int(low[2]), int(high[2]) ):
				yield (x,y,z)

def makeWorldList(state,world,x,y,z):
	listName = hash(repr((world.index,x,y,z)))
	#print (x,y,z)
	#print listName
	WATER = state.reverselookup['water']
	low = Vec3(x,y,z)*state.grain
	hi = Vec3(x+1,y+1,z+1)*state.grain
	glNewList(listName,GL_COMPILE)
	for loc in vrange(low.toTuple(),hi.toTuple()):
		if loc in world.space:
			element = world.space[loc]
			l = Vec3(loc[0],loc[1],loc[2])
			i,j,k = (l-low).toTuple()
			#isWater = element == WATER
			sides = []
			xpos = (loc[0]+1,loc[1]+0,loc[2]+0)
			ypos = (loc[0]+0,loc[1]+1,loc[2]+0)
			zpos = (loc[0]+0,loc[1]+0,loc[2]+1)
			xneg = (loc[0]-1,loc[1]-0,loc[2]-0)
			yneg = (loc[0]-0,loc[1]-1,loc[2]-0)
			zneg = (loc[0]-0,loc[1]-0,loc[2]-1)
			XP = xpos in world.space
			XN = xneg in world.space
			YP = ypos in world.space
			YN = yneg in world.space
			ZP = zpos in world.space
			ZN = zneg in world.space
			XPYP = (loc[0]+1,loc[1]+1,loc[2]+0) in world.space
			XNYP = (loc[0]-1,loc[1]+1,loc[2]+0) in world.space
			XPYN = (loc[0]+1,loc[1]-1,loc[2]+0) in world.space
			XNYN = (loc[0]-1,loc[1]-1,loc[2]+0) in world.space
			XPZP = (loc[0]+1,loc[1]+0,loc[2]+1) in world.space
			XNZP = (loc[0]-1,loc[1]+0,loc[2]+1) in world.space
			XPZN = (loc[0]+1,loc[1]+0,loc[2]-1) in world.space
			XNZN = (loc[0]-1,loc[1]+0,loc[2]-1) in world.space
			YPZP = (loc[0]+0,loc[1]+1,loc[2]+1) in world.space
			YNZP = (loc[0]+0,loc[1]-1,loc[2]+1) in world.space
			YPZN = (loc[0]+0,loc[1]+1,loc[2]-1) in world.space
			YNZN = (loc[0]+0,loc[1]-1,loc[2]-1) in world.space
			XPYPZP = (loc[0]+1,loc[1]+1,loc[2]+1) in world.space
			XNYPZP = (loc[0]-1,loc[1]+1,loc[2]+1) in world.space
			XPYNZP = (loc[0]+1,loc[1]-1,loc[2]+1) in world.space
			XNYNZP = (loc[0]-1,loc[1]-1,loc[2]+1) in world.space
			XPYPZN = (loc[0]+1,loc[1]+1,loc[2]-1) in world.space
			XNYPZN = (loc[0]-1,loc[1]+1,loc[2]-1) in world.space
			XPYNZN = (loc[0]+1,loc[1]-1,loc[2]-1) in world.space
			XNYNZN = (loc[0]-1,loc[1]-1,loc[2]-1) in world.space
			
			# faces
			if not XP:
				sides.append( state.XPOS )
				if YP and not XPYP: sides.append(state.FACE_XPOS_YP)
				if YP and XPYP: sides.append(state.FACE_XPOS_YP_O)
				if YN and not XPYN: sides.append(state.FACE_XPOS_YN)
				if YN and XPYN: sides.append(state.FACE_XPOS_YN_O)
				if ZP and not XPZP: sides.append(state.FACE_XPOS_ZP)
				if ZP and XPZP: sides.append(state.FACE_XPOS_ZP_O)
				if ZN and not XPZN: sides.append(state.FACE_XPOS_ZN)
				if ZN and XPZN: sides.append(state.FACE_XPOS_ZN_O)
				if YP and ZP and YPZP and not XPYPZP and not XPYP and not XPZP: sides.append(state.FACE_XPOS_YPZP)
				if YP and ZN and YPZN and not XPYPZN and not XPYP and not XPZN: sides.append(state.FACE_XPOS_YPZN)
				if YN and ZP and YNZP and not XPYNZP and not XPYP and not XPZP: sides.append(state.FACE_XPOS_YNZP)
				if YN and ZN and YNZN and not XPYNZN and not XPYP and not XPZN: sides.append(state.FACE_XPOS_YNZN)
				if YP and ZP and not YPZP and not XPYPZP and not XPYP and not XPZP: sides.append(state.FACE_XPOS_YPZPT)
				if YP and ZN and not YPZN and not XPYPZN and not XPYP and not XPZN: sides.append(state.FACE_XPOS_YPZNT)
				if YN and ZP and not YNZP and not XPYNZP and not XPYN and not XPZP: sides.append(state.FACE_XPOS_YNZPT)
				if YN and ZN and not YNZN and not XPYNZN and not XPYN and not XPZN: sides.append(state.FACE_XPOS_YNZNT)

			if not XN:
				sides.append( state.XNEG )
				if YP and not XNYP: sides.append(state.FACE_XNEG_YP)
				if YP and XNYP: sides.append(state.FACE_XNEG_YP_O)
				if YN and not XNYN: sides.append(state.FACE_XNEG_YN)
				if YN and XNYN: sides.append(state.FACE_XNEG_YN_O)
				if ZP and not XNZP: sides.append(state.FACE_XNEG_ZP)
				if ZP and XNZP: sides.append(state.FACE_XNEG_ZP_O)
				if ZN and not XNZN: sides.append(state.FACE_XNEG_ZN)
				if ZN and XNZN: sides.append(state.FACE_XNEG_ZN_O)
				if YP and ZP and YPZP and not XNYPZP and not XNYP and not XNZP: sides.append(state.FACE_XNEG_YPZP)
				if YP and ZN and YPZN and not XNYPZN and not XNYP and not XNZN: sides.append(state.FACE_XNEG_YPZN)
				if YN and ZP and YNZP and not XNYNZP and not XNYP and not XNZP: sides.append(state.FACE_XNEG_YNZP)
				if YN and ZN and YNZN and not XNYNZN and not XNYP and not XNZN: sides.append(state.FACE_XNEG_YNZN)
				if YP and ZP and not YPZP and not XNYPZP and not XNYP and not XNZP: sides.append(state.FACE_XNEG_YPZPT)
				if YP and ZN and not YPZN and not XNYPZN and not XNYP and not XNZN: sides.append(state.FACE_XNEG_YPZNT)
				if YN and ZP and not YNZP and not XNYNZP and not XNYN and not XNZP: sides.append(state.FACE_XNEG_YNZPT)
				if YN and ZN and not YNZN and not XNYNZN and not XNYN and not XNZN: sides.append(state.FACE_XNEG_YNZNT)

			if not YP:
				sides.append( state.YPOS )
				if XP and not XPYP: sides.append(state.FACE_YPOS_XP)
				if XP and XPYP: sides.append(state.FACE_YPOS_XP_O)
				if XN and not XNYP: sides.append(state.FACE_YPOS_XN)
				if XN and XNYP: sides.append(state.FACE_YPOS_XN_O)
				if ZP and not YPZP: sides.append(state.FACE_YPOS_ZP)
				if ZP and YPZP: sides.append(state.FACE_YPOS_ZP_O)
				if ZN and not YPZN: sides.append(state.FACE_YPOS_ZN)
				if ZN and YPZN: sides.append(state.FACE_YPOS_ZN_O)
				if XP and ZP and XPZP and not XPYPZP and not XPYP and not YPZP: sides.append(state.FACE_YPOS_XPZP)
				if XP and ZN and XPZN and not XPYPZN and not XPYP and not YPZN: sides.append(state.FACE_YPOS_XPZN)
				if XN and ZP and XNZP and not XNYPZP and not XNYP and not YPZP: sides.append(state.FACE_YPOS_XNZP)
				if XN and ZN and XNZN and not XNYPZN and not XNYP and not YPZN: sides.append(state.FACE_YPOS_XNZN)
				if XP and ZP and not XPZP and not XPYPZP and not XPYP and not YPZP: sides.append(state.FACE_YPOS_XPZPT)
				if XP and ZN and not XPZN and not XPYPZN and not XPYP and not YPZN: sides.append(state.FACE_YPOS_XPZNT)
				if XN and ZP and not XNZP and not XNYPZP and not XNYP and not YPZP: sides.append(state.FACE_YPOS_XNZPT)
				if XN and ZN and not XNZN and not XNYPZN and not XNYP and not YPZN: sides.append(state.FACE_YPOS_XNZNT)

			if not YN:
				sides.append( state.YNEG )
				if XP and not XPYN: sides.append(state.FACE_YNEG_XP)
				if XP and XPYN: sides.append(state.FACE_YNEG_XP_O)
				if XN and not XNYN: sides.append(state.FACE_YNEG_XN)
				if XN and XNYN: sides.append(state.FACE_YNEG_XN_O)
				if ZP and not YNZP: sides.append(state.FACE_YNEG_ZP)
				if ZP and YNZP: sides.append(state.FACE_YNEG_ZP_O)
				if ZN and not YNZN: sides.append(state.FACE_YNEG_ZN)
				if ZN and YNZN: sides.append(state.FACE_YNEG_ZN_O)
				if XP and ZP and XPZP and not XPYNZP and not XPYN and not YNZP: sides.append(state.FACE_YNEG_XPZP)
				if XP and ZN and XPZN and not XPYNZN and not XPYN and not YNZN: sides.append(state.FACE_YNEG_XPZN)
				if XN and ZP and XNZP and not XNYNZP and not XNYN and not YNZP: sides.append(state.FACE_YNEG_XNZP)
				if XN and ZN and XNZN and not XNYNZN and not XNYN and not YNZN: sides.append(state.FACE_YNEG_XNZN)
				if XP and ZP and not XPZP and not XPYNZP and not XPYN and not YNZP: sides.append(state.FACE_YNEG_XPZPT)
				if XP and ZN and not XPZN and not XPYNZN and not XPYN and not YNZN: sides.append(state.FACE_YNEG_XPZNT)
				if XN and ZP and not XNZP and not XNYNZP and not XNYN and not YNZP: sides.append(state.FACE_YNEG_XNZPT)
				if XN and ZN and not XNZN and not XNYNZN and not XNYN and not YNZN: sides.append(state.FACE_YNEG_XNZNT)

			if not ZP:
				sides.append( state.ZPOS )
				if XP and not XPZP: sides.append(state.FACE_ZPOS_XP)
				if XP and XPZP: sides.append(state.FACE_ZPOS_XP_O)
				if XN and not XNZP: sides.append(state.FACE_ZPOS_XN)
				if XN and XNZP: sides.append(state.FACE_ZPOS_XN_O)
				if YP and not YPZP: sides.append(state.FACE_ZPOS_YP)
				if YP and YPZP: sides.append(state.FACE_ZPOS_YP_O)
				if YN and not YNZP: sides.append(state.FACE_ZPOS_YN)
				if YN and YNZP: sides.append(state.FACE_ZPOS_YN_O)
				if XP and YP and XPYP and not XPYPZP and not XPZP and not YPZP: sides.append(state.FACE_ZPOS_XPYP)
				if XP and YN and XPYN and not XPYNZP and not XPZP and not YNZP: sides.append(state.FACE_ZPOS_XPYN)
				if XN and YP and XNYP and not XNYPZP and not XNZP and not YPZP: sides.append(state.FACE_ZPOS_XNYP)
				if XN and YN and XNYN and not XNYNZP and not XNZP and not YNZP: sides.append(state.FACE_ZPOS_XNYN)
				if XP and YP and not XPYP and not XPYPZP and not XPZP and not YPZP: sides.append(state.FACE_ZPOS_XPYPT)
				if XP and YN and not XPYN and not XPYNZP and not XPZP and not YNZP: sides.append(state.FACE_ZPOS_XPYNT)
				if XN and YP and not XNYP and not XNYPZP and not XNZP and not YPZP: sides.append(state.FACE_ZPOS_XNYPT)
				if XN and YN and not XNYN and not XNYNZP and not XNZP and not YNZP: sides.append(state.FACE_ZPOS_XNYNT)

			if not ZN:
				sides.append( state.ZNEG )
				if XP and not XPZN: sides.append(state.FACE_ZNEG_XP)
				if XP and XPZN: sides.append(state.FACE_ZNEG_XP_O)
				if XN and not XNZN: sides.append(state.FACE_ZNEG_XN)
				if XN and XNZN: sides.append(state.FACE_ZNEG_XN_O)
				if YP and not YPZN: sides.append(state.FACE_ZNEG_YP)
				if YP and YPZN: sides.append(state.FACE_ZNEG_YP_O)
				if YN and not YNZN: sides.append(state.FACE_ZNEG_YN)
				if YN and YNZN: sides.append(state.FACE_ZNEG_YN_O)
				if XP and YP and XPYP and not XPYPZN and not XPZN and not YPZN: sides.append(state.FACE_ZNEG_XPYP)
				if XP and YN and XPYN and not XPYNZN and not XPZN and not YNZN: sides.append(state.FACE_ZNEG_XPYN)
				if XN and YP and XNYP and not XNYPZN and not XNZN and not YPZN: sides.append(state.FACE_ZNEG_XNYP)
				if XN and YN and XNYN and not XNYNZN and not XNZN and not YNZN: sides.append(state.FACE_ZNEG_XNYN)
				if XP and YP and not XPYP and not XPYPZN and not XPZN and not YPZN: sides.append(state.FACE_ZNEG_XPYPT)
				if XP and YN and not XPYN and not XPYNZN and not XPZN and not YNZN: sides.append(state.FACE_ZNEG_XPYNT)
				if XN and YP and not XNYP and not XNYPZN and not XNZN and not YPZN: sides.append(state.FACE_ZNEG_XNYPT)
				if XN and YN and not XNYN and not XNYNZN and not XNZN and not YNZN: sides.append(state.FACE_ZNEG_XNYNT)
			
			# edges
			if not XP:
				if not YP:
					sides.append(state.EDGE_XPYP)
					if ZP: sides.append(state.EDGE_XPYP_ZP)
					if ZN: sides.append(state.EDGE_XPYP_ZN)
				if not YN:
					sides.append(state.EDGE_XPYN)
					if ZP: sides.append(state.EDGE_XPYN_ZP)
					if ZN: sides.append(state.EDGE_XPYN_ZN)
				if not ZP:
					sides.append(state.EDGE_XPZP)
					if YP: sides.append(state.EDGE_XPZP_YP)
					if YN: sides.append(state.EDGE_XPZP_YN)
				if not ZN:
					sides.append(state.EDGE_XPZN)
					if YP: sides.append(state.EDGE_XPZN_YP)
					if YN: sides.append(state.EDGE_XPZN_YN)

			if not XN:
				if not YP:
					sides.append(state.EDGE_XNYP)
					if ZP: sides.append(state.EDGE_XNYP_ZP)
					if ZN: sides.append(state.EDGE_XNYP_ZN)
				if not YN:
					sides.append(state.EDGE_XNYN)
					if ZP: sides.append(state.EDGE_XNYN_ZP)
					if ZN: sides.append(state.EDGE_XNYN_ZN)
				if not ZP:
					sides.append(state.EDGE_XNZP)
					if YP: sides.append(state.EDGE_XNZP_YP)
					if YN: sides.append(state.EDGE_XNZP_YN)
				if not ZN:
					sides.append(state.EDGE_XNZN)
					if YP: sides.append(state.EDGE_XNZN_YP)
					if YN: sides.append(state.EDGE_XNZN_YN)

			if not YP:
				if not XP: sides.append(state.EDGE_XPYP)
				if not XN: sides.append(state.EDGE_XNYP)
				if not ZP:
					sides.append(state.EDGE_YPZP)
					if XP: sides.append(state.EDGE_YPZP_XP)
					if XN: sides.append(state.EDGE_YPZP_XN)
				if not ZN:
					sides.append(state.EDGE_YPZN)
					if XP: sides.append(state.EDGE_YPZN_XP)
					if XN: sides.append(state.EDGE_YPZN_XN)

			if not YN:
				if not XP: sides.append(state.EDGE_XPYN)
				if not XN: sides.append(state.EDGE_XNYN)
				if not ZP:
					sides.append(state.EDGE_YNZP)
					if XP: sides.append(state.EDGE_YNZP_XP)
					if XN: sides.append(state.EDGE_YNZP_XN)
				if not ZN:
					sides.append(state.EDGE_YNZN)
					if XP: sides.append(state.EDGE_YNZN_XP)
					if XN: sides.append(state.EDGE_YNZN_XN)

			if not ZP:
				if not XP: sides.append(state.EDGE_XPZP)
				if not XN: sides.append(state.EDGE_XNZP)
				if not YP: sides.append(state.EDGE_YPZP)
				if not YN: sides.append(state.EDGE_YNZP)

			if not ZN:
				if not XP: sides.append(state.EDGE_XPZN)
				if not XN: sides.append(state.EDGE_XNZN)
				if not YP: sides.append(state.EDGE_YPZN)
				if not YN: sides.append(state.EDGE_YNZN)

			# corners
			if not XP and not YP and not ZP: sides.append(state.CORNER_XPYPZP)
			if not XN and not YP and not ZP: sides.append(state.CORNER_XNYPZP)
			if not XP and not YN and not ZP: sides.append(state.CORNER_XPYNZP)
			if not XN and not YN and not ZP: sides.append(state.CORNER_XNYNZP)
			if not XP and not YP and not ZN: sides.append(state.CORNER_XPYPZN)
			if not XN and not YP and not ZN: sides.append(state.CORNER_XNYPZN)
			if not XP and not YN and not ZN: sides.append(state.CORNER_XPYNZN)
			if not XN and not YN and not ZN: sides.append(state.CORNER_XNYNZN)

			
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
					state.draw_face(side, True, 1.0, 0.6)

				glEnd()
				glPopMatrix()
	glEndList()
	return listName
state.makeWorldList = lambda world,x,y,z : makeWorldList(state, world,x,y,z)
	
def updateWorldList(state,world,adjusted):
	x,y,z = adjusted
	potential = []
	for X in range(x-1,x+2):
		for Y in range( y-1, y+2 ):
			for Z in range( z-1, z+2):
				potential.append((X,Y,Z))
	state.refreshFor( world, potential )
state.updateWorldList = lambda w,a : updateWorldList(state,w,a)

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
		stuff.space = state.worlds[0].space
		stuff.numworlds = len(state.worlds)
		stuff.world = {}
		for w in range(1,len(state.worlds)):
			world = state.worlds[w]
			stuff.world[w] = ( world.space, world.pos, world.yaw )
		stuff.playerpos = state.playerpos
		stuff.playeraimyaw = state.playeraimyaw
		stuff.playeraimpitch = state.playeraimpitch
		f = open(filename,'wb')
		pickle.dump(stuff,f)
		f.close()
		f = open('bin'+filename,'wb')
		f.write( struct.pack( "fffff",state.playerpos.x,state.playerpos.y,state.playerpos.z,state.playeraimyaw,state.playeraimpitch) )
		f.write( struct.pack( "i", len(stuff.space.keys() ) ) )
		for key, value in stuff.space.items():
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
	state.worlds[0].space = stuff.space
	if hasattr(stuff, 'numworlds'):
		numworlds = stuff.numworlds
		for w in range(1,numworlds):
			state.worlds.append( WorldState() )
			state.worlds[w].space, state.worlds[w].pos, state.worlds[w].yaw = stuff.world[w]
			state.worlds[w].chunks = {}
			state.worlds[w].index = w
	if stuff.playerpos: state.playerpos = stuff.playerpos
	if stuff.playeraimyaw: state.playeraimyaw = stuff.playeraimyaw
	if stuff.playeraimpitch: state.playeraimpitch = stuff.playeraimpitch
	update(0)
except IOError:
	pass


# Direct OpenGL commands to this window.
window = pyglet.window.Window()
#window = pyglet.window.Window( width = 1024 )
state.width,state.height = window.get_size()
#print state.width, state.height

window.set_exclusive_mouse(True)
state.menu = 0
def toggleMenu(state):
	state.menu = 1-state.menu
	if state.menu == 0:
		window.set_exclusive_mouse(True)
	else:
		window.set_exclusive_mouse(False)
		state.playercontrol = Vec3(0,0,0)
state.toggleMenu = lambda : toggleMenu(state)

def refreshFor( state, world, cells ):
	todo = {}
	#print len( space )
	for k in cells:
		t=(int(k[0]/state.grain),int(k[1]/state.grain),int(k[2]/state.grain))
		todo[t] = True
	#print len( todo )
	for k in todo.keys():
		#print k
		world.chunks[k] = state.makeWorldList(world,k[0],k[1],k[2])
state.refreshFor = lambda w,c: refreshFor(state, w, c )

for world in state.worlds:
	state.refreshFor( world, world.space.keys() )

def updateFromAllSpace(state):
	for world in state.worlds:
		state.refreshFor( world, world.space.keys())
state.updateFromAllSpace = lambda : updateFromAllSpace(state)

def storeOldState(state,world,cells):
	memo = {}
	for k in cells:
		if k in world.space:
			memo[k] = world.space[k]
		else:
			memo[k] = 0
	state.memo = memo
	state.memoworld = world
state.StoreForUndo = lambda w,c : storeOldState(state,w,c)
def restoreOldState(state):
	if state.memo != None:
		world = state.memoworld
		for k,v in state.memo.items():
			if v == 0:
				if k in world.space:
					del world.space[k]
			else:
				world.space[k] = v
		state.refreshFor( world, state.memo.keys())
		state.memo = None
		state.memoworld = None
state.Undo = lambda : restoreOldState( state )

def changeMaterial( state, inc ):
	state.plonk = state.plonk - inc
	while state.plonk < 1:
		state.plonk = state.plonk + state.MAX_ID
	while state.plonk > state.MAX_ID:
		state.plonk = state.plonk - state.MAX_ID
state.changeMaterial = lambda i : changeMaterial( state, i )

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
	if state.mode == state.MODE_DRIVING: # driving mode
		if state.currentWorld != state.worlds[0]:
			state.currentWorld.yaw = state.currentWorld.yaw + yaw
state.changeaim = lambda y,p: changeaim(state,y,p)

@window.event
def on_mouse_motion(x, y, dx, dy):
	game_on_mouse_motion(state, x, y, dx, dy )

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	game_on_mouse_motion(state, x, y, dx, dy )

@window.event
def on_mouse_press(x,y, buttons, modifiers):
	game_on_mouse_press(state, x, y, buttons, modifiers)

@window.event
def on_mouse_release(x,y, buttons, modifiers):
	game_on_mouse_release(state, x, y, buttons, modifiers)

from controls import *
	
@window.event
def on_key_press(symbol, modifiers):
	return game_on_key_press(state,symbol, modifiers)

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
