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
			
def addprocgentostate(state):
	state.updateProcGen = updateProcGen

