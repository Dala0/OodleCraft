#drawing
from pyglet.gl import *

def game_on_draw( s ):
	glEnable(GL_DEPTH_TEST)
	#shader.bind()
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	gluPerspective(70,s.width*1.0/s.height,0.01,1000)
	targetLook = s.playerpos + s.playeraim
	gluLookAt(s.playerpos.x,s.playerpos.y,s.playerpos.z, targetLook.x,targetLook.y,targetLook.z, 0,1,0)

	glClearColor(0.5, 0.8, 0.9, 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)

	# fallback

	glColor3f(1,1,1)

	glLoadIdentity()
	# the elements of space

	for location, element in s.chunks.items():
		glPushMatrix()
		i,j,k = location[0],location[1],location[2]
		glTranslatef(i*s.grain,j*s.grain,k*s.grain)
		glCallList(element)
		glPopMatrix()
	if s.aimpair:
		glPushMatrix()
		loc,dest = s.aimpair
		direc = ( dest[0]-loc[0], dest[1]-loc[1], dest[2]-loc[2] )
		i,j,k = loc[0],loc[1],loc[2]
		glTranslatef(i,j,k)
		glScalef(0.5,0.5,0.5)
		glColor4f(1.0,0.0,0.0,0.5)
		texture = s.textures[s.plonk]
		glEnable(texture.target)
		glBindTexture(texture.target,texture.id)
		glCallList(s.cutList[direc])
		glPopMatrix()
		
	for name, player in s.players.items():
		glPushMatrix()
		glTranslatef(player.pos.x,player.pos.y,player.pos.z)
		glCallList(s.CUBE)
		glPopMatrix()
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	w = s.width / 2
	h = s.height / 2
	glOrtho(-w,w,-h,h,-1,1);
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	if s.mode == 0:
		glColor4f(1.0,1.0,1.0,0.9)
		glScalef(16.0,16.0,0.1)
		glEnable(s.cursortexture.target)
		glBindTexture(s.cursortexture.target,s.cursortexture.id)
		glCallList(s.ZNEG)

	glDisable(GL_DEPTH_TEST)
	glLoadIdentity()
	glTranslatef(8+16-w,8+16-h,0)
	glScalef(16.0,16.0,0.1)
	texture = s.textures[s.plonk]
	glEnable(texture.target)
	glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glBindTexture(texture.target,texture.id)
	glCallList(s.ZNEG)
	
	glLoadIdentity()
	glTranslatef(8+16+16+8-w,8+16-h,0)
	glPushMatrix()
	glColor4f(0,0,0,0.5)
	s.glyph_string.draw()
	glTranslatef(0,2,0)
	s.glyph_string.draw()
	glTranslatef(2,0,0)
	s.glyph_string.draw()
	glTranslatef(0,-2,0)
	s.glyph_string.draw()
	glPopMatrix()		
	glTranslatef(1,1,0)
	glColor4f(1.0,1.0,1.0,1.0)
	s.glyph_string.draw()

