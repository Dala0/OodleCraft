from vec import *

def intersects( cubeAt, rayStart, rayDir ):
	range = 10
	cubeCentre = Vec3( cubeAt[0], cubeAt[1], cubeAt[2] )
	cubePos = cubeCentre - rayStart
	if abs(cubePos) > range:
		return None
	distance = cubePos.dot(rayDir)
	#print "distance: ",distance
	if distance > range or distance < 0:
		return None
	xDiff = (1,0,0)
	yDiff = (0,1,0)
	zDiff = (0,0,1)
	xt1,xt2,yt1,yt2,zt1,zt2 = 0,range,0,range,0,range
	if abs( rayDir.x ) > 0:
		xt1 = (cubePos.x+0.5)/rayDir.x
		xt2 = (cubePos.x-0.5)/rayDir.x
		if xt2 < xt1:
			xt1,xt2 = xt2,xt1
			xDiff = (-1,0,0)
	#print "xt: ",xt1," ",xt2,
	if abs( rayDir.y ) > 0:
		yt1 = (cubePos.y+0.5)/rayDir.y
		yt2 = (cubePos.y-0.5)/rayDir.y
		if yt2 < yt1:
			yt1,yt2 = yt2,yt1
			yDiff = (0,-1,0)
	#print " yt: ",yt1," ",yt2,
	if abs( rayDir.z ) > 0:
		zt1 = (cubePos.z+0.5)/rayDir.z
		zt2 = (cubePos.z-0.5)/rayDir.z
		if zt2 < zt1:
			zt1,zt2 = zt2,zt1
			zDiff = (0,0,-1)
	#print " zt: ",zt1," ",zt2,
	maxMin = xt1
	diff = xDiff
	if yt1 > maxMin:
		maxMin = yt1
		diff = yDiff
	if zt1 > maxMin:
		maxMin = zt1
		diff = zDiff
	minMax = xt2
	if yt2 < minMax: minMax = yt2
	if zt2 < minMax: minMax = zt2
	#print " MXM&d: ",maxMin," ",minMax," ",diff
	if maxMin < minMax:
		return maxMin,diff
	return None

def bounds( low, hi, target ):
	if hi.x <= target.x or low.x > target.x:
		return False
	if hi.y <= target.y or low.y > target.y:
		return False
	if hi.z <= target.z or low.z > target.z:
		return False
	return True

