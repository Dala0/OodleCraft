import math

class Vec3:
	def __init__(self, initx, inity, initz):
		self.x = float(initx)
		self.y = float(inity)
		self.z = float(initz)
	def XY(self):
		return (int(self.x),int(self.y))
	def __str__(self):
		return '(%s,%s,%s)' % (self.x, self.y, self.z)
	def __repr__(self):
		return 'Vec3(%s,%s,%s)' % (self.x, self.y, self.z)
	def __add__(self, other):
		return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
	def __sub__(self, other):
		return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)        
	def __mul__(self, scale):
		return Vec3(scale * self.x, scale * self.y, scale * self.z)
	def __div__(self, div):
		return Vec3(self.x/div, self.y/div, self.z/div)

	def dot(self, other):
		return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
	def __abs__(self):
		return math.sqrt(self.dot(self))
	def cross(self, other):
		return Vec3(self.y * other.z - self.z * other.y,
			self.z * other.x - self.x * other.z,
			self.x * other.y - self.y * other.x)
	def crossY(self):
		return Vec3( self.z, 0, -self.x )
	def normalized(self):
		return self * (1.0 / abs(self))
	def normalize(self):
		mod = 1.0 / self.magnitude()
		self.x *= mod
		self.x *= mod
		self.x *= mod
	def __neg__(self):
		return Vec3(-self.x, -self.y, -self.z)

	def __eq__(self, other):
		return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

	def bounce(self, normal):
		d = normal * self.dot(normal)
		return self - d * 2
	def clampmag(self, to):
		l = abs(self)
		if l > to:
			l = l / to
			self.x /= l
			self.y /= l
			self.z /= l
	def clamp(self, to):
		if self.x > to:
			self.x = to
		elif self.x < -to:
			self.x = -to
		if self.y > to:
			self.y = to
		elif self.y < -to:
			self.y = -to
		if self.z > to:
			self.z = to
		elif self.z < -to:
			self.z = -to
	def toTuple(self):
		return (self.x,self.y,self.z)

Vec3.ZERO = Vec3(0,0,0)
Vec3.RIGHT = Vec3(1,0,0)
Vec3.UP = Vec3(0,1,0)
Vec3.OUT = Vec3(0,0,1)

def S2V( s ):
	v = s.split(',')
	return Vec3(v[0],v[1],v[2])
def T2V( v ):
	return Vec3(v[0],v[1],v[2])

def isVector( element ):
	try:
		nums = element.split(',')
		x,y,z = float(nums[0]),float(nums[1]),float(nums[2])
		return True
	except:
		pass
	return False

assert ( S2V( '5,4,3' ) - Vec3( 5,4,2 ) ) == Vec3(0,0,1)
assert ( T2V( (5,4,3) ) - Vec3( 5,4,2 ) ) == Vec3(0,0,1)

assert Vec3.RIGHT.bounce(Vec3.UP) == Vec3.RIGHT
assert Vec3(-1,-1,0).bounce(Vec3.UP) == Vec3(-1,1,0)
assert Vec3(0.5,0.0,0.0).normalized() == Vec3(1,0,0)
c = Vec3(2,0,0)
c.clampmag(1)
assert c == Vec3(1,0,0)

