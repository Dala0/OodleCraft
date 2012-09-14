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
	gluLookAt(s.playerpos.x,s.playerpos.y+1,s.playerpos.z, targetLook.x,targetLook.y+1,targetLook.z, 0,1,0)

	glClearColor(0.5, 0.8, 0.9, 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)

	# fallback

	glColor3f(1,1,1)

	glLoadIdentity()
	# the elements of space

	for world in s.worlds:
		for location, element in world.chunks.items():
			glPushMatrix()
			i,j,k = location[0],location[1],location[2]
			glTranslatef(world.pos.x,world.pos.y,world.pos.z)
			glRotatef(180.0*world.yaw/3.14159,0,1,0)
			glTranslatef(i*s.grain,j*s.grain,k*s.grain)
			glCallList(element)
			glPopMatrix()
	if s.hasMovedSinceStartedClicking and s.inInsert:
		glPushMatrix()
		world = s.worlds[s.mouse_action_start[2]]
		start = s.mouse_action_start[1]
		end = s.getInAirPoint()
		scale = map(lambda x:0.5*abs(x[0]-x[1])+0.51,zip(end,start))
		mid = map(lambda x:(x[0]+x[1])*0.5,zip(end,start))
		glTranslatef(world.pos.x,world.pos.y,world.pos.z)
		glRotatef(180.0*world.yaw/3.14159,0,1,0)
		glTranslatef(mid[0],mid[1],mid[2])
		glScalef(scale[0],scale[1],scale[2])
		glColor4f(1.0,0.0,0.0,0.5)
		texture = s.textures[s.plonk]
		glEnable(texture.target)
		glBindTexture(texture.target,texture.id)
		glCallList(s.UNLITCUBE)
		glPopMatrix()
	elif s.hasMovedSinceStartedClicking and s.inDelete:
		glPushMatrix()
		world = s.worlds[s.mouse_action_start[2]]
		start = s.mouse_action_start[0]
		end = s.getInAirPoint()
		scale = map(lambda x:0.5*abs(x[0]-x[1])+0.51,zip(end,start))
		mid = map(lambda x:(x[0]+x[1])*0.5,zip(end,start))
		glTranslatef(world.pos.x,world.pos.y,world.pos.z)
		glRotatef(180.0*world.yaw/3.14159,0,1,0)
		glTranslatef(mid[0],mid[1],mid[2])
		glScalef(scale[0],scale[1],scale[2])
		glColor4f(1.0,0.0,0.0,0.5)
		texture = s.textures[s.plonk]
		glEnable(texture.target)
		glBindTexture(texture.target,texture.id)
		glCallList(s.UNLITCUBE)
		glPopMatrix()
	elif s.aimpair:
		glPushMatrix()
		loc,dest,w,d = s.aimpair
		world = s.worlds[w]
		if s.mouse_action_start != None:
			start = dest
			end = s.mouse_action_start[1]
			if s.inDelete:
				start = loc
				end = s.mouse_action_start[0]
			scale = map(lambda x:0.5*abs(x[0]-x[1])+0.51,zip(end,start))
			mid = map(lambda x:(x[0]+x[1])*0.5,zip(end,start))
			glTranslatef(world.pos.x,world.pos.y,world.pos.z)
			glRotatef(180.0*world.yaw/3.14159,0,1,0)
			glTranslatef(mid[0],mid[1],mid[2])
			glScalef(scale[0],scale[1],scale[2])
			glColor4f(1.0,0.0,0.0,0.5)
			texture = s.textures[s.plonk]
			glEnable(texture.target)
			glBindTexture(texture.target,texture.id)
			glCallList(s.UNLITCUBE)
			glPopMatrix()
		else:
			glTranslatef(world.pos.x,world.pos.y,world.pos.z)
			glRotatef(180.0*world.yaw/3.14159,0,1,0)
			direc = ( dest[0]-loc[0], dest[1]-loc[1], dest[2]-loc[2] )
			i,j,k = loc[0],loc[1],loc[2]
			glTranslatef(i,j,k)
			glScalef(0.5,0.5,0.5)
			glColor4f(1.0,0.0,0.0,0.5)
			texture = s.textures[s.plonk]
			glEnable(texture.target)
			glBindTexture(texture.target,texture.id)
			s.cutList[direc]()
			#glCallList(s.cutList[direc])
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
	if s.menu == 0: # fly around and edit mode
		glColor4f(1.0,1.0,1.0,0.9)
		glScalef(16.0,16.0,0.1)
		glEnable(s.cursortexture.target)
		glBindTexture(s.cursortexture.target,s.cursortexture.id)
		s.draw_ZNEG()
		#glCallList(s.ZNEG)
	
	glColor4f(1.0,1.0,1.0,0.9)
	glDisable(GL_DEPTH_TEST)
	glLoadIdentity()
	glTranslatef(8+16-w,8+16-h,0)
	glScalef(16.0,16.0,0.1)
	texture = s.textures[s.plonk]
	glEnable(texture.target)
	glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glBindTexture(texture.target,texture.id)
	s.draw_ZNEG()
	#glCallList(s.ZNEG)
	
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

	count = len(s.debuglog)
	for index,item in enumerate(s.debuglog):
		glPushMatrix()
		glLoadIdentity()
		string = item[0]
		glyphs = item[1]
		xpos = w-glyphs.get_subwidth(0,len(string))
		ypos = h-10 * (count-index)
		glTranslatef(xpos,ypos,0)
		glyphs.draw()
		glPopMatrix()

	if s.menu == 1: # command mode, where the mouse is given freedom.
		invcols = s.invwcount
		invrows = 1 + (s.MAX_ID-1) / 8
		gap = s.invs+s.invb
		invw = invcols * gap + s.invb
		invh = invrows * gap + s.invb

		glColor4f(0,0,0,0.5)
		glLoadIdentity()
		glTranslatef(s.invx+invw/2-w,h-s.invy-invh/2,0)
		glScalef(invw/2,invh/2,0.1)
		texture = s.textures[s.reverselookup['black']]
		glEnable(texture.target)
		glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glBindTexture(texture.target,texture.id)
		s.draw_ZNEG()
		#glCallList(s.ZNEG)

		glColor4f(1.0,1.0,1.0,1.0)
		for i in range(s.MAX_ID):
			i = i + 1
			if i in s.textures:
				x = i % 8
				y = i / 8
				glLoadIdentity()
				glTranslatef(s.invx+s.invb+16-w+x*40,h-s.invy-s.invb-16-y*40,0)
				glScalef(16.0,16.0,0.1)
				texture = s.textures[i]
				glEnable(texture.target)
				glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
				glBindTexture(texture.target,texture.id)
				s.draw_ZNEG()
				#glCallList(s.ZNEG)


