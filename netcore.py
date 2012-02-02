import threading
import sys, time
import socket

SIOCGIFCONF = 0x8912  #define SIOCGIFCONF
BYTES = 4096          # Simply define the byte size

def joiners(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.settimeout(1)
	#print "binding joiners to ", ('', core.BPORT)
	s.bind(('', core.BPORT))
	while True:
		try:
			message, address = s.recvfrom(1024)
			if not address[0] == core.hostip:
				#print "Got data from", address, ":", message
				if not address in core.peers:
					core.peers.append(address)
				if message == 'ping':
					# Acknowledge it.
					core.broadcastable.append( "me" )
		except socket.timeout:
			pass

def messagers(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.settimeout(1)
	#print "binding messagers to ",('', core.CPORT)
	s.bind(('', core.CPORT))
	while True:
		try:
			message, address = s.recvfrom(1024)
			#print "Got data from", address, ":", message
			core.recvd.append( message )
		except socket.timeout:
			pass

def broadcastPusher(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	#print "binding broadcast to ",core.hostip
	s.bind((core.hostip, core.BPORT))
	while True:
		if len( core.broadcastable ) > 0:
			data = core.broadcastable[0]
			#print 'broadasting ',data
			s.sendto(data, ('<broadcast>', core.BPORT))
			core.broadcastable = core.broadcastable[1:]
		else:
			time.sleep(1)

def messagePusher(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	while True:
		if len( core.sendable ) > 0:
			data = core.sendable[0]
			#print 'sending',data
			for dest in core.peers:
				#print 'to ',dest
				s.sendto(data, (dest[0],core.CPORT))
			core.sendable = core.sendable[1:]
		else:
			time.sleep(0.01)

def get_ip_list():
	try:
		import array
		import struct
		import fcntl
		sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		names = array.array('B', '\0' * BYTES)
		bytelen = struct.unpack('iL', fcntl.ioctl(sck.fileno(), SIOCGIFCONF, struct.pack('iL', BYTES, names.buffer_info()[0])))[0]
		namestr = names.tostring()
		a = [namestr[i:i+32] for i in range(0, bytelen, 32)]
		ips = [ n[20:24] for n in a ]
		b = ['.'.join( [str(ord(e)) for e in n ] ) for n in ips ]
		b.remove( '127.0.0.1' )
		return b
	except ImportError:
		#meh, windows
		pass
	return [socket.gethostbyname(socket.gethostname())]

class netcore:
	def __init__(self):
		self.peers = []
		self.broadcastable = ['ping']
		self.sendable = []
		self.recvd = []
		self.hostip = get_ip_list()[0]
		self.BPORT = 50000
		self.CPORT = 50002
		j = threading.Thread(target=joiners,args=[self])
		j.daemon = True
		j.start()
		l = threading.Thread(target=messagers,args=[self])
		l.daemon = True
		l.start()
		bpusher = threading.Thread(target=broadcastPusher,args=[self])
		bpusher.daemon = True
		bpusher.start()
		mpusher = threading.Thread(target=messagePusher,args=[self])
		mpusher.daemon = True
		mpusher.start()
	def send(self, message):
		self.sendable.append( message )
	def recvall(self):
		r = self.recvd
		self.recvd = []
		return r
	def recv(self):
		if len( recvd ) > 0:
			r = self.recvd[0]
			self.recvd = self.recvd[1:]
			return r
		else:
			return None

