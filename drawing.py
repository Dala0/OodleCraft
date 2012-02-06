#drawing
from pyglet.gl import *

def game_on_draw( scope ):
	glEnable(GL_DEPTH_TEST)
	#shader.bind()
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	width = scope['width']
	height = scope['height']

	gluPerspective(70,width*1.0/height,0.01,1000)
	playerpos = scope['playerpos']
	playeraim = scope['playeraim']
	targetLook = playerpos + playeraim
	gluLookAt(playerpos.x,playerpos.y,playerpos.z, targetLook.x,targetLook.y,targetLook.z, 0,1,0)

	glClearColor(0.5, 0.8, 0.9, 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)

	# fallback

	glColor3f(1,1,1)

	glLoadIdentity()
	# the elements of space

	grain = scope['grain']
	chunks = scope['chunks']
	for location, element in chunks.items():
		glPushMatrix()
		i,j,k = location[0],location[1],location[2]
		glTranslatef(i*grain,j*grain,k*grain)
		glCallList(element)
		glPopMatrix()
	aimpair = scope['aimpair']
	cutList = scope['cutList']
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
		
	players = scope['players']
	for name, player in players.items():
		glPushMatrix()
		glTranslatef(player.pos.x,player.pos.y,player.pos.z)
		glCallList(CUBE)
		glPopMatrix()
	
	cursortexture = scope['cursortexture']

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
	glCallList(scope['ZNEG'])

	plonk = scope['plonk']
	textures = scope['textures']

	glDisable(GL_DEPTH_TEST)
	glLoadIdentity()
	glTranslatef(8+16-w,8+16-h,0)
	glScalef(16.0,16.0,0.1)
	texture = textures[plonk]
	glEnable(texture.target)
	glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glBindTexture(texture.target,texture.id)
	glCallList(scope['ZNEG'])
	
	glyph_string = scope['glyph_string']
	
	glLoadIdentity()
	glTranslatef(8+16+16+8-w,8+16-h,0)
	glPushMatrix()
	glColor4f(0,0,0,0.5)
	glyph_string.draw()
	glTranslatef(0,2,0)
	glyph_string.draw()
	glTranslatef(2,0,0)
	glyph_string.draw()
	glTranslatef(0,-2,0)
	glyph_string.draw()
	glPopMatrix()		
	glTranslatef(1,1,0)
	glColor4f(1.0,1.0,1.0,1.0)
	glyph_string.draw()

