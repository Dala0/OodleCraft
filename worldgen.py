import random
r = random.Random()
r.seed( 321 )

#world is x +left y +down

def hashIt( hashableValue ):
	key = 0
	for character in hashableValue:
		oc = ord(character)
		key = ( key + oc ) % 0x100000000
		key = ( key + ( key << 10 ) ) % 0x100000000
		key = ( key ^ ( key >> 6 ) ) % 0x100000000
	key = ( key + ( key << 3 ) ) % 0x100000000
	key = ( key ^ ( key >> 11 ) ) % 0x100000000
	key = ( key + ( key << 15 ) ) % 0x100000000
	if key < 2:
		key = ( key + 2 ) % 0x100000000
	return key


def within( a, b, distance ):
	d = (a[0]-b[0], a[1]-b[1])
	ds = d[0]*d[0] + d[1]*d[1]
	return distance*distance >= ds

def noise( x, level, salt ):
	n = hashIt( str(x)+':'+str(level)+str(salt) )
	n = ( ( n / 64 ) & 127 ) - 63
	return n

hlist = {}
def perlin3d( x, y, z, level, minlevel, salt ):
	global hlist
	address = str((x,y,z))+','+str(level)+','+str(salt)
	try:
		h = hlist[ address ]
		return h
	except KeyError:
		h = 0
		for i in range( minlevel, level ):
			ax = x>>i
			ay = y>>i
			az = z>>i
			ox = ax<<i
			oy = ay<<i
			oz = az<<i
			dx = x-ox
			dy = y-oy
			dz = z-oz
			dm = 1<<i
			ah = noise( (ax, ay, az), i, salt )
			bh = noise( (ax+1, ay, az), i, salt )
			ch = noise( (ax, ay+1, az), i, salt )
			dh = noise( (ax+1, ay+1, az), i, salt )
			lh = ( ah * (dm-dx) + bh * dx ) / dm
			hh = ( ch * (dm-dx) + dh * dx ) / dm
			l1 = ( lh * (dm-dy) + hh * dy ) / dm
			ah = noise( (ax, ay, az+1), i, salt )
			bh = noise( (ax+1, ay, az+1), i, salt )
			ch = noise( (ax, ay+1, az+1), i, salt )
			dh = noise( (ax+1, ay+1, az+1), i, salt )
			lh = ( ah * (dm-dx) + bh * dx ) / dm
			hh = ( ch * (dm-dx) + dh * dx ) / dm
			l2 = ( lh * (dm-dy) + hh * dy ) / dm
			fh = ( l1 * (dm-dz) + l2 * dz ) / dm
			h += fh
			h *= 0.5
		hlist[ address ] = h
		return h
		
def perlin2d( x, y, level, minlevel, salt ):
	global hlist

	address = str((x,y))+','+str(level)+','+str(salt)
	try:
		h = hlist[ address ]
		return h
	except KeyError:
		h = 0
		for i in range( minlevel, level ):
			ax = x>>i
			ay = y>>i
			ox = ax<<i
			oy = ay<<i
			dx = x-ox
			dy = y-oy
			dm = 1<<i
			ah = noise( (ax, ay), i, salt )
			bh = noise( (ax+1, ay), i, salt )
			ch = noise( (ax, ay+1), i, salt )
			dh = noise( (ax+1, ay+1), i, salt )
			lh = ( ah * (dm-dx) + bh * dx ) / dm
			hh = ( ch * (dm-dx) + dh * dx ) / dm
			fh = ( lh * (dm-dy) + hh * dy ) / dm
			h += fh
			h *= 0.5
		hlist[ address ] = h
		return h
	
hlist = {}
def perlin1( x, level, salt ):
	global hlist
	address = str(x)+'a'+str(level)+'a'+str(salt)
	try:
		h = hlist[ address ]
		return h
	except KeyError:
		h = 0
		for i in range( level ):
			ax = x>>i
			ox = ax<<i
			dx = x-ox
			dm = 1<<i
			ah = noise( ax, i, salt )
			bh = noise( ax+1, i, salt )
			lh = ( ah * (dm-dx) + bh * dx ) / dm
			h += lh
			h *= 0.5
		hlist[ address ] = h
		return h		
	
def worldheight( x, salt ):
	return perlin( x, 8, salt )

ores = {}

def generateworld( location, salt ):
	value = 'stone' # stone
	x = location[0]
	y = location[1]
	z = location[2]
	originx = x - (( x % 32 + 32 ) % 32 )
	originy = y - (( y % 32 + 32 ) % 32 )
	cellx = originx / 32
	celly = originy / 32
	offset = (x-originx, y-originy)

	h = 0
	if y < 128 or y > -128:
		h = perlin2d( x,z, 8,4, salt )

	depth = h-y
	if depth < 0:
		if y >= 0:
			value = None
		else:
			value = 'water'
	else:
		if depth < 6:
			value = 'dirt'
		if depth < 2:
			value = 'grass'
		if depth < 3 and y<0:
			value = 'sand'

	r = random.Random()

	#if it's currently sky, then it could be a tree
	if value == 'sky' and depth > -16:
		for xa in range( -1, 2 ):
			cellhash = hashIt( str(cellx+xa)+':'+str(salt) )
			r.seed( cellhash & 32767 )
			numtrees = int(r.random()*3+2)
			for i in range( numtrees ):
				height = int(r.random()*4+4)
				where = int(r.random()*32)+xa*32
				wh = worldheight( where+originx, salt )
				if wh <= 0:
					base = ( where+originx, wh )
					top = ( base[0], base[1]-height )
					if within( location, top, height/2 ):
						value = LEAF
					if where == offset[0] and top[1] <= location[1]:
						value = WOOD
				
		
	#now, if it's currently stone, it could be an ore... or something else
	if value == 'stone':
		for xa in range( -1, 2 ):
			for ya in range( -1, 2 ):
				address = str(cellx+xa)+','+str(celly+ya)+':'+str(salt)
				orelist = []
				try:
					orelist = ores[ address ]
				except KeyError:
					thiscell = hashIt( address )
					r.seed( thiscell & 32767 )
					for i in range( 5 ):
						thing = r.random()
						where = (int(r.random()*32)+xa*32+originx,int(r.random()*32)+ya*32+originy)
						where2 = (int(r.random()*5)-2,int(r.random()*5)-2)
						where2 = ( where2[0]+where[0], where2[1]+where[1] )
						if thing < 0.4:
							orelist.append( ('coal',where,2,0) )
						elif thing < 0.6:
							orelist.append( ('ironore',where,2,3) )
						elif thing < 0.7:
							orelist.append( ('water',where,5,0) )
							orelist.append( ('water',where2,4,0) )
						elif thing < 0.8:
							orelist.append( ('lava',where,4,10) )
							orelist.append( ('lava',where2,3,10) )
						elif thing < 0.85:
							orelist.append( ('goldore',where,4,20) )
						elif thing < 0.87:
							orelist.append( ('diamondore',where,2,30) )
						else:
							orelist.append( ('cave',where,4,0) )
							orelist.append( ('cave',where2,4,0) )
					ores[ address ] = orelist
				# now use the orelist
				for ore in orelist:
					if within( location, ore[1], ore[2] ) and depth > ore[3]:
						value = ore[0]
	return value
	

