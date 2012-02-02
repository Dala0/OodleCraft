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
	n = hashIt( str(x)+'a'+str(level)+'a'+str(salt) )
	n = ( ( n / 64 ) & 127 ) - 63
	return n
	
hlist = {}
def perlin( x, level, salt ):
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
	value = 0 # stone
	x = location[0]
	y = location[1]
	originx = x - (( x % 32 + 32 ) % 32 )
	originy = y - (( y % 32 + 32 ) % 32 )
	cellx = originx / 32
	celly = originy / 32
	offset = (x-originx, y-originy)

	h = 0
	if y < 128 or y > -128:
		h = perlin( x, 8, salt )

	depth = y - h
	if depth < 0:
		if y <= 0:
			value = SKY
		else:
			value = WATER
	else:
		if depth < 6:
			value = DIRT
		if depth < 2:
			value = GRASS
		if depth < 3 and y>=0:
			value = SAND

	r = random.Random()

	#if it's currently sky, then it could be a tree
	if value == SKY and depth > -16:
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
	if value == STONE:
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
							orelist.append( (COAL,where,2,0) )
						elif thing < 0.6:
							orelist.append( (IRON,where,2,3) )
						elif thing < 0.7:
							orelist.append( (WATER,where,5,0) )
							orelist.append( (WATER,where2,4,0) )
						elif thing < 0.8:
							orelist.append( (LAVA,where,4,10) )
							orelist.append( (LAVA,where2,3,10) )
						elif thing < 0.85:
							orelist.append( (GOLD,where,4,20) )
						elif thing < 0.87:
							orelist.append( (DIAMOND,where,2,30) )
						else:
							orelist.append( (CAVE,where,4,0) )
							orelist.append( (CAVE,where2,4,0) )
					ores[ address ] = orelist
				# now use the orelist
				for ore in orelist:
					if within( location, ore[1], ore[2] ) and depth > ore[3]:
						value = ore[0]
	return value
	

