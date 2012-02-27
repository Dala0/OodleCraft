import threading
import sys, time
import socket

SIOCGIFCONF = 0x8912  #define SIOCGIFCONF
BYTES = 4096          # Simply define the byte size
BPORT = 50000 # broadcast port
CPORT = 50002 # connection port

## the threaded stream recv
def recv_thread(peer):
	s = peer.relSock
	while True:
		#try:
		data = s.recv(4096)
		if not data:
			break
		#print "Got data from", address, ":", message
		peer.rrecv.append( data )
		#except socket.timeout:
		#	pass
	print "recv_thread for ",peer.ip," ended"
	peer.relSock = None
	peer.rt = None
	
## the Peer class for handling the various connections
class Peer:
	def __init__(self, address, s=None):
		if s:
			print "New Peer at ",address," +s"
		else:
			print "New Peer at ",address
		self.usend = []
		self.urecv = []
		self.rsend = []
		self.rrecv = []
		self.ip, self.port = address
		if not s:
			self.relSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "Connect to ",self.ip," : ",CPORT
			self.relSock.connect( (self.ip,CPORT) )
		else:
			self.relSock = s
		# start the recv thread
		self.rt = threading.Thread(target=recv_thread,args=[self])
		self.rt.daemon = True
		self.rt.start()
	def sendReliable( self, message ):
		self.relSock.send( message )
	def getReliable( self ):
		if len( self.rrecv ) > 0:
			returnable = self.rrecv[0]
			self.rrecv = self.rrecv[1:]
			return returnable
		return None
	def urecvall(self):
		r = self.urecv
		self.urecv = []
		return r
	def rrecvall(self):
		r = self.rrecv
		self.rrecv = []
		return r

## incoming reliable connections
def listener(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.settimeout(1)
	#print "binding listener to ", ('', BPORT)
	s.bind(('', CPORT))
	s.listen(3)
	while True:
		try:
			conn, address = s.accept()
			if not address[0] == core.hostip:
				#print "Got connection from", address, ":", message
				a = filter( lambda f: f.ip == address[0], core.peers )
				if len( a ) == 0:			
				#if not address in core.peers:
					core.peers.append(Peer(address,conn))
				else:
					print "dangerous fail ",address
					conn.close()
		except socket.timeout:
			pass

## incoming unreliable data
def messagers(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.settimeout(1)
	#print "binding messagers to ",('', CPORT)
	s.bind(('', CPORT))
	while True:
		try:
			message, address = s.recvfrom(1024)
			for peer in core.peers:
				if peer.ip == address[0]:
					peer.urecv.append( message )
					message = None
					break
		except socket.timeout:
			pass

## broadcast RECV
def joiners(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.settimeout(1)
	#print "binding joiners to ", ('', BPORT)
	s.bind(('', BPORT))
	while True:
		try:
			message, address = s.recvfrom(1024)
			if not address[0] == core.hostip:
				#print "Got data from", address, ":", message
				a = filter( lambda f: f.ip == address[0], core.peers )
				if len( a ) == 0:			
				#if not address in core.peers:
					core.peers.append(Peer(address))
				if message == 'ping':
					# Acknowledge it.
					core.broadcastable.append( "me" )
		except socket.timeout:
			pass

## broadcast SEND
def broadcastPusher(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	#print "binding broadcast to ",core.hostip
	s.bind((core.hostip, BPORT))
	while True:
		if len( core.broadcastable ) > 0:
			data = core.broadcastable[0]
			#print 'broadasting ',data
			s.sendto(data, ('<broadcast>', BPORT))
			core.broadcastable = core.broadcastable[1:]
		else:
			time.sleep(1)

## outgoing message pump
def messagePusher(core):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	while True:
		doneNothing = True
		for peer in core.peers:
			if len( peer.usend ) > 0:
				doneNothing = False
				data = peer.usend[0]
				dest = peer.ip
				#print 'sending',data,' to ',dest
				s.sendto(data, (dest,CPORT))
				peer.usend = peer.usend[1:]
		if doneNothing:	
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

def updater(core):
	while True:
		closers = []
		for peer in core.peers[:]:
			if peer.rt == None and peer.relSock == None:
				# must want to kill this peer
				print "killing peer ",peer.ip
				core.peers.remove(peer)
		time.sleep(1)			

class netcore:
	def __init__(self):
		self.peers = []
		self.broadcastable = ['ping']
		self.hostip = get_ip_list()[0]
		j = threading.Thread(target=joiners,args=[self])
		j.daemon = True
		j.start()
		m = threading.Thread(target=messagers,args=[self])
		m.daemon = True
		m.start()
		l = threading.Thread(target=listener,args=[self])
		l.daemon = True
		l.start()
		bpusher = threading.Thread(target=broadcastPusher,args=[self])
		bpusher.daemon = True
		bpusher.start()
		mpusher = threading.Thread(target=messagePusher,args=[self])
		mpusher.daemon = True
		mpusher.start()
		update = threading.Thread(target=updater,args=[self])
		update.daemon = True
		update.start()
	def send(self, message):
		for peer in self.peers:
			peer.usend.append( message )

