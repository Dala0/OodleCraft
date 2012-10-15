from pyglet.gl import *

CUBE = 1

YPOS = 2
YNEG = 3
XPOS = 4
XNEG = 5
ZPOS = 6
ZNEG = 7
EDGE_XPYP = 8
EDGE_XNYP = 9
EDGE_XPYN = 10
EDGE_XNYN = 11
EDGE_XPZP = 12
EDGE_XNZP = 13
EDGE_XPZN = 14
EDGE_XNZN = 15
EDGE_YPZP = 16
EDGE_YNZP = 17
EDGE_YPZN = 18
EDGE_YNZN = 19
CORNER_XPYPZP = 20
CORNER_XNYPZP = 21
CORNER_XPYNZP = 22
CORNER_XNYNZP = 23
CORNER_XPYPZN = 24
CORNER_XNYPZN = 25
CORNER_XPYNZN = 26
CORNER_XNYNZN = 27
FACE_XPOS_YP = 28
FACE_XPOS_YN = 29
FACE_XPOS_ZP = 30
FACE_XPOS_ZN = 31
FACE_XPOS_YP_O = 32
FACE_XPOS_YN_O = 33
FACE_XPOS_ZP_O = 34
FACE_XPOS_ZN_O = 35
FACE_XPOS_YPZP = 36
FACE_XPOS_YNZP = 37
FACE_XPOS_YPZN = 38
FACE_XPOS_YNZN = 39
FACE_XPOS_YPZPT = 40
FACE_XPOS_YNZPT = 41
FACE_XPOS_YPZNT = 42
FACE_XPOS_YNZNT = 43
FACE_YPOS_XP = 44
FACE_YPOS_XN = 45
FACE_YPOS_ZP = 46
FACE_YPOS_ZN = 47
FACE_YPOS_XP_O = 48
FACE_YPOS_XN_O = 49
FACE_YPOS_ZP_O = 50
FACE_YPOS_ZN_O = 51
FACE_YPOS_XPZP = 52
FACE_YPOS_XNZP = 53
FACE_YPOS_XPZN = 54
FACE_YPOS_XNZN = 55
FACE_YPOS_XPZPT = 56
FACE_YPOS_XNZPT = 57
FACE_YPOS_XPZNT = 58
FACE_YPOS_XNZNT = 59
FACE_ZPOS_XP = 60
FACE_ZPOS_XN = 61
FACE_ZPOS_YP = 62
FACE_ZPOS_YN = 63
FACE_ZPOS_XP_O = 64
FACE_ZPOS_XN_O = 65
FACE_ZPOS_YP_O = 66
FACE_ZPOS_YN_O = 67
FACE_ZPOS_XPYP = 68
FACE_ZPOS_XNYP = 69
FACE_ZPOS_XPYN = 70
FACE_ZPOS_XNYN = 71
FACE_ZPOS_XPYPT = 72
FACE_ZPOS_XNYPT = 73
FACE_ZPOS_XPYNT = 74
FACE_ZPOS_XNYNT = 75
FACE_XNEG_YP = 76
FACE_XNEG_YN = 77
FACE_XNEG_ZP = 78
FACE_XNEG_ZN = 79
FACE_XNEG_YP_O = 80
FACE_XNEG_YN_O = 81
FACE_XNEG_ZP_O = 82
FACE_XNEG_ZN_O = 83
FACE_XNEG_YPZP = 84
FACE_XNEG_YNZP = 85
FACE_XNEG_YPZN = 86
FACE_XNEG_YNZN = 87
FACE_XNEG_YPZPT = 88
FACE_XNEG_YNZPT = 89
FACE_XNEG_YPZNT = 90
FACE_XNEG_YNZNT = 91
FACE_YNEG_XP = 92
FACE_YNEG_XN = 93
FACE_YNEG_ZP = 94
FACE_YNEG_ZN = 95
FACE_YNEG_XP_O = 96
FACE_YNEG_XN_O = 97
FACE_YNEG_ZP_O = 98
FACE_YNEG_ZN_O = 99
FACE_YNEG_XPZP = 100
FACE_YNEG_XNZP = 101
FACE_YNEG_XPZN = 102
FACE_YNEG_XNZN = 103
FACE_YNEG_XPZPT = 104
FACE_YNEG_XNZPT = 105
FACE_YNEG_XPZNT = 106
FACE_YNEG_XNZNT = 107
FACE_ZNEG_XP = 108
FACE_ZNEG_XN = 109
FACE_ZNEG_YP = 110
FACE_ZNEG_YN = 111
FACE_ZNEG_XP_O = 112
FACE_ZNEG_XN_O = 113
FACE_ZNEG_YP_O = 114
FACE_ZNEG_YN_O = 115
FACE_ZNEG_XPYP = 116
FACE_ZNEG_XNYP = 117
FACE_ZNEG_XPYN = 118
FACE_ZNEG_XNYN = 119
FACE_ZNEG_XPYPT = 120
FACE_ZNEG_XNYPT = 121
FACE_ZNEG_XPYNT = 122
FACE_ZNEG_XNYNT = 123
EDGE_XPYP_ZP = 124
EDGE_XPYP_ZN = 125
EDGE_XNYP_ZP = 126
EDGE_XNYP_ZN = 127
EDGE_XPYN_ZP = 128
EDGE_XPYN_ZN = 129
EDGE_XNYN_ZP = 130
EDGE_XNYN_ZN = 131
EDGE_XPZP_YP = 132
EDGE_XPZP_YN = 133
EDGE_XNZP_YP = 134
EDGE_XNZP_YN = 135
EDGE_XPZN_YP = 136
EDGE_XPZN_YN = 137
EDGE_XNZN_YP = 138
EDGE_XNZN_YN = 139
EDGE_YPZP_XP = 140
EDGE_YPZP_XN = 141
EDGE_YPZN_XP = 142
EDGE_YPZN_XN = 143
EDGE_YNZP_XP = 144
EDGE_YNZP_XN = 145
EDGE_YNZN_XP = 146
EDGE_YNZN_XN = 147

UNLITCUBE = 8

o = 1
O = 1.01
k7 = 0.707179
k3 = 0.577321

def draw_cube():
	glColor3f(0.75,0.75,0.75)
	glNormal3f(0,0,-1)
	glTexCoord2f( 0, 0)
	glVertex3f( -o, -o, -o)
	glTexCoord2f( 1, 0)
	glVertex3f(  o, -o, -o)
	glTexCoord2f( 1, 1)
	glVertex3f(  o,  o, -o)
	glTexCoord2f( 0, 1)
	glVertex3f( -o,  o, -o)
	glColor3f(0.8,0.8,0.8)
	glNormal3f(0,0,1)
	glTexCoord2f( 0, 0)
	glVertex3f( -o, -o,  o)
	glTexCoord2f( 1, 0)
	glVertex3f(  o, -o,  o)
	glTexCoord2f( 1, 1)
	glVertex3f(  o,  o,  o)
	glTexCoord2f( 0, 1)
	glVertex3f( -o,  o,  o)
	glColor3f(0.5,0.5,0.5)
	glNormal3f(0,-1,0) 
	glTexCoord2f( 0, 0)
	glVertex3f( -o, -o, -o)
	glTexCoord2f( 1, 0)
	glVertex3f(  o, -o, -o)
	glTexCoord2f( 1, 1)
	glVertex3f(  o, -o,  o)
	glTexCoord2f( 0, 1)
	glVertex3f( -o, -o,  o)
	glColor3f(1.0,1.0,1.0)
	glNormal3f(0,1,0) 
	glTexCoord2f( 0, 0)
	glVertex3f( -o,  o, -o)
	glTexCoord2f( 1, 0)
	glVertex3f(  o,  o, -o)
	glTexCoord2f( 1, 1)
	glVertex3f(  o,  o,  o)
	glTexCoord2f( 0, 1)
	glVertex3f( -o,  o,  o)
	glColor3f(0.85,0.85,0.85)
	glNormal3f(-1,0,0)
	glTexCoord2f( 0, 0)
	glVertex3f( -o, -o, -o)
	glTexCoord2f( 1, 0)
	glVertex3f( -o,  o, -o)
	glTexCoord2f( 1, 1)
	glVertex3f( -o,  o,  o)
	glTexCoord2f( 0, 1)
	glVertex3f( -o, -o,  o)                      
	glColor3f(0.9,0.9,0.9)
	glNormal3f(1,0,0)
	glTexCoord2f( 0, 0)
	glVertex3f(  o, -o, -o)
	glTexCoord2f( 1, 0)
	glVertex3f(  o,  o, -o)
	glTexCoord2f( 1, 1)
	glVertex3f(  o,  o,  o)
	glTexCoord2f( 0, 1)
	glVertex3f(  o, -o,  o)

allcorners = [CORNER_XPYPZP,CORNER_XNYPZP,CORNER_XPYNZP,CORNER_XNYNZP,CORNER_XPYPZN,CORNER_XNYPZN,CORNER_XPYNZN,CORNER_XNYNZN]

def draw_face(face, andColour = True, N=o, R=o):
	if face in allcorners:
		x = 1 if face in [CORNER_XPYPZP,CORNER_XPYNZP,CORNER_XPYPZN,CORNER_XPYNZN] else -1
		y = 1 if face in [CORNER_XPYPZP,CORNER_XNYPZP,CORNER_XPYPZN,CORNER_XNYPZN] else -1
		z = 1 if face in [CORNER_XPYPZP,CORNER_XNYPZP,CORNER_XPYNZP,CORNER_XNYNZP] else -1
		if andColour: glColor3f(0.85,0.85,0.85)
		glNormal3f(x*k3,y*k3,z*k3)
		glTexCoord2f( 1, 0)
		glVertex3f( x*R, y*R, z*N)
		glTexCoord2f( 1, 1)
		glVertex3f( x*R, y*N, z*R)
		glTexCoord2f( 0, 1)
		glVertex3f( x*N, y*R, z*R)
		glTexCoord2f( 0, 0)
		glVertex3f( x*N, y*R, z*R)

	if face in [EDGE_YPZP,EDGE_YPZP_XP,EDGE_YPZP_XN]:
		xn,xp = -R,R
		if face == EDGE_YPZP_XP: xn =  1
		if face == EDGE_YPZP_XN: xp = -1
		if andColour: glColor3f(0.95,0.95,0.95)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f( xn,  R,  N)
		glTexCoord2f( 1, 1)
		glVertex3f( xn,  N,  R)
		glTexCoord2f( 0, 1)
		glVertex3f( xp,  N,  R)
		glTexCoord2f( 0, 0)
		glVertex3f( xp,  R,  N)
	if face in [EDGE_YPZN,EDGE_YPZN_XP,EDGE_YPZN_XN]:
		xn,xp = -R,R
		if face == EDGE_YPZN_XP: xn =  1
		if face == EDGE_YPZN_XN: xp = -1
		if andColour: glColor3f(0.7,0.7,0.7)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f( xn,  R,  -N)
		glTexCoord2f( 1, 1)
		glVertex3f( xn,  N,  -R)
		glTexCoord2f( 0, 1)
		glVertex3f( xp,  N,  -R)
		glTexCoord2f( 0, 0)
		glVertex3f( xp,  R,  -N)
	if face in [EDGE_YNZP,EDGE_YNZP_XP,EDGE_YNZP_XN]:
		xn,xp = -R,R
		if face == EDGE_YNZP_XP: xn =  1
		if face == EDGE_YNZP_XN: xp = -1
		if andColour: glColor3f(0.95,0.95,0.95)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f( xn,  -R,  N)
		glTexCoord2f( 1, 1)
		glVertex3f( xn,  -N,  R)
		glTexCoord2f( 0, 1)
		glVertex3f( xp,  -N,  R)
		glTexCoord2f( 0, 0)
		glVertex3f( xp,  -R,  N)
	if face in [EDGE_YNZN,EDGE_YNZN_XP,EDGE_YNZN_XN]:
		xn,xp = -R,R
		if face == EDGE_YNZN_XP: xn =  1
		if face == EDGE_YNZN_XN: xp = -1
		if andColour: glColor3f(0.7,0.7,0.7)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  xn, -R,  -N)
		glTexCoord2f( 1, 1)
		glVertex3f( xn,  -N,  -R)
		glTexCoord2f( 0, 1)
		glVertex3f( xp,  -N,  -R)
		glTexCoord2f( 0, 0)
		glVertex3f( xp,  -R,  -N)
	if face in [EDGE_XPZP,EDGE_XPZP_YP,EDGE_XPZP_YN]:
		yn,yp = -R,R
		if face == EDGE_XPZP_YP: yn =  1
		if face == EDGE_XPZP_YN: yp = -1
		if andColour: glColor3f(0.95,0.95,0.95)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  R, yn, N)
		glTexCoord2f( 1, 1)
		glVertex3f(  N, yn,  R)
		glTexCoord2f( 0, 1)
		glVertex3f(  N, yp,  R)
		glTexCoord2f( 0, 0)
		glVertex3f(  R, yp,  N)
	if face in [EDGE_XPZN,EDGE_XPZN_YP,EDGE_XPZN_YN]:
		yn,yp = -R,R
		if face == EDGE_XPZN_YP: yn =  1
		if face == EDGE_XPZN_YN: yp = -1
		if andColour: glColor3f(0.7,0.7,0.7)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  R, yn,  -N)
		glTexCoord2f( 1, 1)
		glVertex3f(  N, yn,  -R)
		glTexCoord2f( 0, 1)
		glVertex3f(  N, yp,  -R)
		glTexCoord2f( 0, 0)
		glVertex3f(  R, yp,  -N)
	if face in [EDGE_XNZP,EDGE_XNZP_YP,EDGE_XNZP_YN]:
		yn,yp = -R,R
		if face == EDGE_XNZP_YP: yn =  1
		if face == EDGE_XNZP_YN: yp = -1
		if andColour: glColor3f(0.95,0.95,0.95)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  -R, yn,  N)
		glTexCoord2f( 1, 1)
		glVertex3f(  -N, yn,  R)
		glTexCoord2f( 0, 1)
		glVertex3f(  -N, yp,  R)
		glTexCoord2f( 0, 0)
		glVertex3f(  -R, yp,  N)
	if face in [EDGE_XNZN,EDGE_XNZN_YP,EDGE_XNZN_YN]:
		yn,yp = -R,R
		if face == EDGE_XNZN_YP: yn =  1
		if face == EDGE_XNZN_YN: yp = -1
		if andColour: glColor3f(0.7,0.7,0.7)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  -R, yn,  -N)
		glTexCoord2f( 1, 1)
		glVertex3f(  -N, yn,  -R)
		glTexCoord2f( 0, 1)
		glVertex3f(  -N, yp,  -R)
		glTexCoord2f( 0, 0)
		glVertex3f(  -R, yp,  -N)
	if face in [EDGE_XPYP,EDGE_XPYP_ZP,EDGE_XPYP_ZN]:
		zn,zp = -R,R
		if face == EDGE_XPYP_ZP: zn =  1
		if face == EDGE_XPYP_ZN: zp = -1
		if andColour: glColor3f(0.95,0.95,0.95)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  R,  N, zn)
		glTexCoord2f( 1, 1)
		glVertex3f(  N,  R, zn)
		glTexCoord2f( 0, 1)
		glVertex3f(  N,  R, zp)
		glTexCoord2f( 0, 0)
		glVertex3f(  R,  N, zp)
	if face in [EDGE_XPYN,EDGE_XPYN_ZP,EDGE_XPYN_ZN]:
		zn,zp = -R,R
		if face == EDGE_XPYN_ZP: zn =  1
		if face == EDGE_XPYN_ZN: zp = -1
		if andColour: glColor3f(0.7,0.7,0.7)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  R,  -N, zn)
		glTexCoord2f( 1, 1)
		glVertex3f(  N,  -R, zn)
		glTexCoord2f( 0, 1)
		glVertex3f(  N,  -R, zp)
		glTexCoord2f( 0, 0)
		glVertex3f(  R,  -N, zp)
	if face in [EDGE_XNYP,EDGE_XNYP_ZP,EDGE_XNYP_ZN]:
		zn,zp = -R,R
		if face == EDGE_XNYP_ZP: zn =  1
		if face == EDGE_XNYP_ZN: zp = -1
		if andColour: glColor3f(0.95,0.95,0.95)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  -R,  N, zn)
		glTexCoord2f( 1, 1)
		glVertex3f(  -N,  R, zn)
		glTexCoord2f( 0, 1)
		glVertex3f(  -N,  R, zp)
		glTexCoord2f( 0, 0)
		glVertex3f(  -R,  N, zp)
	if face in [EDGE_XNYN,EDGE_XNYN_ZP,EDGE_XNYN_ZN]:
		zn,zp = -R,R
		if face == EDGE_XNYN_ZP: zn =  1
		if face == EDGE_XNYN_ZN: zp = -1
		if andColour: glColor3f(0.7,0.7,0.7)
		glNormal3f(k7,k7,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  -R,  -N, zn)
		glTexCoord2f( 1, 1)
		glVertex3f(  -N,  -R, zn)
		glTexCoord2f( 0, 1)
		glVertex3f(  -N,  -R, zp)
		glTexCoord2f( 0, 0)
		glVertex3f(  -R,  -N, zp)

	if face in [ZNEG,FACE_ZNEG_XP,FACE_ZNEG_XN,FACE_ZNEG_YP,FACE_ZNEG_YN,FACE_ZNEG_XPYP,FACE_ZNEG_XNYP,FACE_ZNEG_XPYN,FACE_ZNEG_XNYN]:
		xn,xp,yn,yp = -R,R,-R,R
		if face in [FACE_ZNEG_XP,FACE_ZNEG_XPYP,FACE_ZNEG_XPYN]: xn =  1
		if face in [FACE_ZNEG_XN,FACE_ZNEG_XNYP,FACE_ZNEG_XNYN]: xp = -1
		if face in [FACE_ZNEG_YP,FACE_ZNEG_XPYP,FACE_ZNEG_XNYP]: yn =  1
		if face in [FACE_ZNEG_YN,FACE_ZNEG_XPYN,FACE_ZNEG_XNYN]: yp = -1
		if andColour: glColor3f(0.75,0.75,0.75)
		glNormal3f(0,0,-1)
		glTexCoord2f( 0, 0)
		glVertex3f( xn, yn, -N)
		glTexCoord2f( 1, 0)
		glVertex3f( xp, yn, -N)
		glTexCoord2f( 1, 1)
		glVertex3f( xp, yp, -N)
		glTexCoord2f( 0, 1)
		glVertex3f( xn, yp, -N)
	if face in [ZPOS,FACE_ZPOS_XP,FACE_ZPOS_XN,FACE_ZPOS_YP,FACE_ZPOS_YN,FACE_ZPOS_XPYP,FACE_ZPOS_XNYP,FACE_ZPOS_XPYN,FACE_ZPOS_XNYN]:
		xn,xp,yn,yp = -R,R,-R,R
		if face in [FACE_ZPOS_XP,FACE_ZPOS_XPYP,FACE_ZPOS_XPYN]: xn =  1
		if face in [FACE_ZPOS_XN,FACE_ZPOS_XNYP,FACE_ZPOS_XNYN]: xp = -1
		if face in [FACE_ZPOS_YP,FACE_ZPOS_XPYP,FACE_ZPOS_XNYP]: yn =  1
		if face in [FACE_ZPOS_YN,FACE_ZPOS_XPYN,FACE_ZPOS_XNYN]: yp = -1
		if andColour: glColor3f(0.8,0.8,0.8)
		glNormal3f(0,0,1)
		glTexCoord2f( 0, 0)
		glVertex3f( xn, yn,  N)
		glTexCoord2f( 1, 0)
		glVertex3f( xp, yn,  N)
		glTexCoord2f( 1, 1)
		glVertex3f( xp, yp,  N)
		glTexCoord2f( 0, 1)
		glVertex3f( xn, yp,  N)
	if face in [YNEG,FACE_YNEG_XP,FACE_YNEG_XN,FACE_YNEG_ZP,FACE_YNEG_ZN,FACE_YNEG_XPZP,FACE_YNEG_XNZP,FACE_YNEG_XPZN,FACE_YNEG_XNZN]:
		xn,xp,zn,zp = -R,R,-R,R
		if face in [FACE_YNEG_XP,FACE_YNEG_XPZP,FACE_YNEG_XPZN]: xn =  1
		if face in [FACE_YNEG_XN,FACE_YNEG_XNZP,FACE_YNEG_XNZN]: xp = -1
		if face in [FACE_YNEG_ZP,FACE_YNEG_XPZP,FACE_YNEG_XNZP]: zn =  1
		if face in [FACE_YNEG_ZN,FACE_YNEG_XPZN,FACE_YNEG_XNZN]: zp = -1
		if andColour: glColor3f(0.5,0.5,0.5)
		glNormal3f(0,-1,0) 
		glTexCoord2f( 0, 0)
		glVertex3f( xn, -N, zn)
		glTexCoord2f( 1, 0)
		glVertex3f( xp, -N, zn)
		glTexCoord2f( 1, 1)
		glVertex3f( xp, -N, zp)
		glTexCoord2f( 0, 1)
		glVertex3f( xn, -N, zp)
	if face in [YPOS,FACE_YPOS_XP,FACE_YPOS_XN,FACE_YPOS_ZP,FACE_YPOS_ZN,FACE_YPOS_XPZP,FACE_YPOS_XNZP,FACE_YPOS_XPZN,FACE_YPOS_XNZN]:
		xn,xp,zn,zp = -R,R,-R,R
		if face in [FACE_YPOS_XP,FACE_YPOS_XPZP,FACE_YPOS_XPZN]: xn =  1
		if face in [FACE_YPOS_XN,FACE_YPOS_XNZP,FACE_YPOS_XNZN]: xp = -1
		if face in [FACE_YPOS_ZP,FACE_YPOS_XPZP,FACE_YPOS_XNZP]: zn =  1
		if face in [FACE_YPOS_ZN,FACE_YPOS_XPZN,FACE_YPOS_XNZN]: zp = -1
		if andColour: glColor3f(1.0,1.0,1.0)
		glNormal3f(0,1,0) 
		glTexCoord2f( 0, 0)
		glVertex3f( xn,  N, zn)
		glTexCoord2f( 1, 0)
		glVertex3f( xp,  N, zn)
		glTexCoord2f( 1, 1)
		glVertex3f( xp,  N, zp)
		glTexCoord2f( 0, 1)
		glVertex3f( xn,  N, zp)
	if face in [XNEG,FACE_XNEG_YP,FACE_XNEG_YN,FACE_XNEG_ZP,FACE_XNEG_ZN,FACE_XNEG_YPZP,FACE_XNEG_YNZP,FACE_XNEG_YPZN,FACE_XNEG_YNZN]:
		yn,yp,zn,zp = -R,R,-R,R
		if face in [FACE_XNEG_YP,FACE_XNEG_YPZP,FACE_XNEG_YPZN]: yn =  1
		if face in [FACE_XNEG_YN,FACE_XNEG_YNZP,FACE_XNEG_YNZN]: yp = -1
		if face in [FACE_XNEG_ZP,FACE_XNEG_YPZP,FACE_XNEG_YNZP]: zn =  1
		if face in [FACE_XNEG_ZN,FACE_XNEG_YPZN,FACE_XNEG_YNZN]: zp = -1
		if andColour: glColor3f(0.85,0.85,0.85)
		glNormal3f(-1,0,0)
		glTexCoord2f( 1, 0)
		glVertex3f( -N, yn, zn)
		glTexCoord2f( 1, 1)
		glVertex3f( -N, yp, zn)
		glTexCoord2f( 0, 1)
		glVertex3f( -N, yp, zp)
		glTexCoord2f( 0, 0)
		glVertex3f( -N, yn, zp)                      
	if face in [XPOS,FACE_XPOS_YP,FACE_XPOS_YN,FACE_XPOS_ZP,FACE_XPOS_ZN,FACE_XPOS_YPZP,FACE_XPOS_YNZP,FACE_XPOS_YPZN,FACE_XPOS_YNZN]:
		yn,yp,zn,zp = -R,R,-R,R
		if face in [FACE_XPOS_YP,FACE_XPOS_YPZP,FACE_XPOS_YPZN]: yn =  1
		if face in [FACE_XPOS_YN,FACE_XPOS_YNZP,FACE_XPOS_YNZN]: yp = -1
		if face in [FACE_XPOS_ZP,FACE_XPOS_YPZP,FACE_XPOS_YNZP]: zn =  1
		if face in [FACE_XPOS_ZN,FACE_XPOS_YPZN,FACE_XPOS_YNZN]: zp = -1
		if andColour: glColor3f(0.9,0.9,0.9)
		glNormal3f(1,0,0)
		glTexCoord2f( 1, 0)
		glVertex3f(  N, yn, zn)
		glTexCoord2f( 1, 1)
		glVertex3f(  N, yp, zn)
		glTexCoord2f( 0, 1)
		glVertex3f(  N, yp, zp)
		glTexCoord2f( 0, 0)
		glVertex3f(  N, yn, zp)

	if face == FACE_YPOS_XP_O:
		d = (1-R)/2
		if andColour: glColor3f(1.0,1.0,1.0)
		glNormal3f(0,1,0) 
		glTexCoord2f( 0, 0)
		glVertex3f(  1-d,  d+N, -R)
		glTexCoord2f( 1, 0)
		glVertex3f(  R,  N, -R)
		glTexCoord2f( 1, 1)
		glVertex3f(  R,  N,  R)
		glTexCoord2f( 0, 1)
		glVertex3f(  1-d,  d+N,  R)

	if face == FACE_YPOS_XPZPT:
		if andColour: glColor3f(1.0,1.0,1.0)
		glNormal3f(0,1,0) 
		glTexCoord2f( 0, 0)
		glVertex3f(  R,  N,  1)
		glTexCoord2f( 1, 0)
		glVertex3f(  R,  N,  1)
		glTexCoord2f( 1, 1)
		glVertex3f(  R,  N,  R)
		glTexCoord2f( 0, 1)
		glVertex3f(  1,  N,  R)
	if face == FACE_YPOS_XNZPT:
		if andColour: glColor3f(1.0,1.0,1.0)
		glNormal3f(0,1,0) 
		glTexCoord2f( 0, 0)
		glVertex3f( -R,  N,  1)
		glTexCoord2f( 1, 0)
		glVertex3f( -R,  N,  1)
		glTexCoord2f( 1, 1)
		glVertex3f( -1,  N,  R)
		glTexCoord2f( 0, 1)
		glVertex3f( -R,  N,  R)
	if face == FACE_YPOS_XPZNT:
		if andColour: glColor3f(1.0,1.0,1.0)
		glNormal3f(0,1,0) 
		glTexCoord2f( 0, 0)
		glVertex3f(  1,  N, -R)
		glTexCoord2f( 1, 0)
		glVertex3f(  R,  N, -R)
		glTexCoord2f( 1, 1)
		glVertex3f(  R,  N, -1)
		glTexCoord2f( 0, 1)
		glVertex3f(  R,  N, -1)
	if face == FACE_YPOS_XNZNT:
		if andColour: glColor3f(1.0,1.0,1.0)
		glNormal3f(0,1,0) 
		glTexCoord2f( 0, 0)
		glVertex3f( -R,  N, -R)
		glTexCoord2f( 1, 0)
		glVertex3f( -1,  N, -R)
		glTexCoord2f( 1, 1)
		glVertex3f( -R,  N, -1)
		glTexCoord2f( 0, 1)
		glVertex3f( -R,  N, -1)

glNewList(CUBE,GL_COMPILE)
glBegin(GL_QUADS)
glColor3f(0.75,0.75,0.75)
glNormal3f(0,0,-1)
glTexCoord2f( 0, 0)
glVertex3f( -o, -o, -o)
glTexCoord2f( 1, 0)
glVertex3f(  o, -o, -o)
glTexCoord2f( 1, 1)
glVertex3f(  o,  o, -o)
glTexCoord2f( 0, 1)
glVertex3f( -o,  o, -o)
glColor3f(0.8,0.8,0.8)
glNormal3f(0,0,1)
glTexCoord2f( 0, 0)
glVertex3f( -o, -o,  o)
glTexCoord2f( 1, 0)
glVertex3f(  o, -o,  o)
glTexCoord2f( 1, 1)
glVertex3f(  o,  o,  o)
glTexCoord2f( 0, 1)
glVertex3f( -o,  o,  o)
glColor3f(0.5,0.5,0.5)
glNormal3f(0,-1,0) 
glTexCoord2f( 0, 0)
glVertex3f( -o, -o, -o)
glTexCoord2f( 1, 0)
glVertex3f(  o, -o, -o)
glTexCoord2f( 1, 1)
glVertex3f(  o, -o,  o)
glTexCoord2f( 0, 1)
glVertex3f( -o, -o,  o)
glColor3f(1.0,1.0,1.0)
glNormal3f(0,1,0) 
glTexCoord2f( 0, 0)
glVertex3f( -o,  o, -o)
glTexCoord2f( 1, 0)
glVertex3f(  o,  o, -o)
glTexCoord2f( 1, 1)
glVertex3f(  o,  o,  o)
glTexCoord2f( 0, 1)
glVertex3f( -o,  o,  o)
glColor3f(0.85,0.85,0.85)
glNormal3f(-1,0,0)
glTexCoord2f( 0, 0)
glVertex3f( -o, -o, -o)
glTexCoord2f( 1, 0)
glVertex3f( -o,  o, -o)
glTexCoord2f( 1, 1)
glVertex3f( -o,  o,  o)
glTexCoord2f( 0, 1)
glVertex3f( -o, -o,  o)                      
glColor3f(0.9,0.9,0.9)
glNormal3f(1,0,0)
glTexCoord2f( 0, 0)
glVertex3f(  o, -o, -o)
glTexCoord2f( 1, 0)
glVertex3f(  o,  o, -o)
glTexCoord2f( 1, 1)
glVertex3f(  o,  o,  o)
glTexCoord2f( 0, 1)
glVertex3f(  o, -o,  o)
glEnd()
glEndList()

glNewList(UNLITCUBE,GL_COMPILE)
glBegin(GL_QUADS)
glNormal3f(0,0,-1)
glTexCoord2f( 0, 0)
glVertex3f( -o, -o, -o)
glTexCoord2f( 1, 0)
glVertex3f(  o, -o, -o)
glTexCoord2f( 1, 1)
glVertex3f(  o,  o, -o)
glTexCoord2f( 0, 1)
glVertex3f( -o,  o, -o)
glNormal3f(0,0,1)
glTexCoord2f( 0, 0)
glVertex3f( -o, -o,  o)
glTexCoord2f( 1, 0)
glVertex3f(  o, -o,  o)
glTexCoord2f( 1, 1)
glVertex3f(  o,  o,  o)
glTexCoord2f( 0, 1)
glVertex3f( -o,  o,  o)
glNormal3f(0,-1,0) 
glTexCoord2f( 0, 0)
glVertex3f( -o, -o, -o)
glTexCoord2f( 1, 0)
glVertex3f(  o, -o, -o)
glTexCoord2f( 1, 1)
glVertex3f(  o, -o,  o)
glTexCoord2f( 0, 1)
glVertex3f( -o, -o,  o)
glNormal3f(0,1,0) 
glTexCoord2f( 0, 0)
glVertex3f( -o,  o, -o)
glTexCoord2f( 1, 0)
glVertex3f(  o,  o, -o)
glTexCoord2f( 1, 1)
glVertex3f(  o,  o,  o)
glTexCoord2f( 0, 1)
glVertex3f( -o,  o,  o)
glNormal3f(-1,0,0)
glTexCoord2f( 0, 0)
glVertex3f( -o, -o, -o)
glTexCoord2f( 1, 0)
glVertex3f( -o,  o, -o)
glTexCoord2f( 1, 1)
glVertex3f( -o,  o,  o)
glTexCoord2f( 0, 1)
glVertex3f( -o, -o,  o)                      
glNormal3f(1,0,0)
glTexCoord2f( 0, 0)
glVertex3f(  o, -o, -o)
glTexCoord2f( 1, 0)
glVertex3f(  o,  o, -o)
glTexCoord2f( 1, 1)
glVertex3f(  o,  o,  o)
glTexCoord2f( 0, 1)
glVertex3f(  o, -o,  o)
glEnd()
glEndList()

def draw_XNEG():
	glBegin(GL_QUADS)
	draw_face(XNEG,False,O)
	glEnd()
def draw_XPOS():
	glBegin(GL_QUADS)
	draw_face(XPOS,False,O)
	glEnd()
def draw_YNEG():
	glBegin(GL_QUADS)
	draw_face(YNEG,False,O)
	glEnd()
def draw_YPOS():
	glBegin(GL_QUADS)
	draw_face(YPOS,False,O)
	glEnd()
def draw_ZNEG():
	glBegin(GL_QUADS)
	draw_face(ZNEG,False,O)
	glEnd()
def draw_ZPOS():
	glBegin(GL_QUADS)
	draw_face(ZPOS,False,O)
	glEnd()

def filloutPrims( state ):
	state.draw_face = draw_face
	state.draw_XNEG = draw_XNEG
	state.draw_XPOS = draw_XPOS
	state.draw_YNEG = draw_YNEG
	state.draw_YPOS = draw_YPOS
	state.draw_ZNEG = draw_ZNEG
	state.draw_ZPOS = draw_ZPOS
	state.CUBE = CUBE
	state.UNLITCUBE = UNLITCUBE
	state.YPOS = YPOS
	state.YNEG = YNEG
	state.XPOS = XPOS
	state.XNEG = XNEG
	state.ZPOS = ZPOS
	state.ZNEG = ZNEG
	state.EDGE_XPYP = EDGE_XPYP
	state.EDGE_XNYP = EDGE_XNYP
	state.EDGE_XPYN = EDGE_XPYN
	state.EDGE_XNYN = EDGE_XNYN
	state.EDGE_XPZP = EDGE_XPZP
	state.EDGE_XNZP = EDGE_XNZP
	state.EDGE_XPZN = EDGE_XPZN
	state.EDGE_XNZN = EDGE_XNZN
	state.EDGE_YPZP = EDGE_YPZP
	state.EDGE_YNZP = EDGE_YNZP
	state.EDGE_YPZN = EDGE_YPZN
	state.EDGE_YNZN = EDGE_YNZN
	state.CORNER_XPYPZP = CORNER_XPYPZP
	state.CORNER_XNYPZP = CORNER_XNYPZP
	state.CORNER_XPYNZP = CORNER_XPYNZP
	state.CORNER_XNYNZP = CORNER_XNYNZP
	state.CORNER_XPYPZN = CORNER_XPYPZN
	state.CORNER_XNYPZN = CORNER_XNYPZN
	state.CORNER_XPYNZN = CORNER_XPYNZN
	state.CORNER_XNYNZN = CORNER_XNYNZN
	state.FACE_XPOS_YP = FACE_XPOS_YP
	state.FACE_XPOS_YN = FACE_XPOS_YN
	state.FACE_XPOS_ZP = FACE_XPOS_ZP
	state.FACE_XPOS_ZN = FACE_XPOS_ZN
	state.FACE_XPOS_YP_O = FACE_XPOS_YP_O
	state.FACE_XPOS_YN_O = FACE_XPOS_YN_O
	state.FACE_XPOS_ZP_O = FACE_XPOS_ZP_O
	state.FACE_XPOS_ZN_O = FACE_XPOS_ZN_O
	state.FACE_XPOS_YPZP = FACE_XPOS_YPZP
	state.FACE_XPOS_YNZP = FACE_XPOS_YNZP
	state.FACE_XPOS_YPZN = FACE_XPOS_YPZN
	state.FACE_XPOS_YNZN = FACE_XPOS_YNZN
	state.FACE_XPOS_YPZPT = FACE_XPOS_YPZPT
	state.FACE_XPOS_YNZPT = FACE_XPOS_YNZPT
	state.FACE_XPOS_YPZNT = FACE_XPOS_YPZNT
	state.FACE_XPOS_YNZNT = FACE_XPOS_YNZNT
	state.FACE_YPOS_XP = FACE_YPOS_XP
	state.FACE_YPOS_XN = FACE_YPOS_XN
	state.FACE_YPOS_ZP = FACE_YPOS_ZP
	state.FACE_YPOS_ZN = FACE_YPOS_ZN
	state.FACE_YPOS_XP_O = FACE_YPOS_XP_O
	state.FACE_YPOS_XN_O = FACE_YPOS_XN_O
	state.FACE_YPOS_ZP_O = FACE_YPOS_ZP_O
	state.FACE_YPOS_ZN_O = FACE_YPOS_ZN_O
	state.FACE_YPOS_XPZP = FACE_YPOS_XPZP
	state.FACE_YPOS_XNZP = FACE_YPOS_XNZP
	state.FACE_YPOS_XPZN = FACE_YPOS_XPZN
	state.FACE_YPOS_XNZN = FACE_YPOS_XNZN
	state.FACE_YPOS_XPZPT = FACE_YPOS_XPZPT
	state.FACE_YPOS_XNZPT = FACE_YPOS_XNZPT
	state.FACE_YPOS_XPZNT = FACE_YPOS_XPZNT
	state.FACE_YPOS_XNZNT = FACE_YPOS_XNZNT
	state.FACE_ZPOS_XP = FACE_ZPOS_XP
	state.FACE_ZPOS_XN = FACE_ZPOS_XN
	state.FACE_ZPOS_YP = FACE_ZPOS_YP
	state.FACE_ZPOS_YN = FACE_ZPOS_YN
	state.FACE_ZPOS_XP_O = FACE_ZPOS_XP_O
	state.FACE_ZPOS_XN_O = FACE_ZPOS_XN_O
	state.FACE_ZPOS_YP_O = FACE_ZPOS_YP_O
	state.FACE_ZPOS_YN_O = FACE_ZPOS_YN_O
	state.FACE_ZPOS_XPYP = FACE_ZPOS_XPYP
	state.FACE_ZPOS_XNYP = FACE_ZPOS_XNYP
	state.FACE_ZPOS_XPYN = FACE_ZPOS_XPYN
	state.FACE_ZPOS_XNYN = FACE_ZPOS_XNYN
	state.FACE_ZPOS_XPYPT = FACE_ZPOS_XPYPT
	state.FACE_ZPOS_XNYPT = FACE_ZPOS_XNYPT
	state.FACE_ZPOS_XPYNT = FACE_ZPOS_XPYNT
	state.FACE_ZPOS_XNYNT = FACE_ZPOS_XNYNT
	state.FACE_XNEG_YP = FACE_XNEG_YP
	state.FACE_XNEG_YN = FACE_XNEG_YN
	state.FACE_XNEG_ZP = FACE_XNEG_ZP
	state.FACE_XNEG_ZN = FACE_XNEG_ZN
	state.FACE_XNEG_YP_O = FACE_XNEG_YP_O
	state.FACE_XNEG_YN_O = FACE_XNEG_YN_O
	state.FACE_XNEG_ZP_O = FACE_XNEG_ZP_O
	state.FACE_XNEG_ZN_O = FACE_XNEG_ZN_O
	state.FACE_XNEG_YPZP = FACE_XNEG_YPZP
	state.FACE_XNEG_YNZP = FACE_XNEG_YNZP
	state.FACE_XNEG_YPZN = FACE_XNEG_YPZN
	state.FACE_XNEG_YNZN = FACE_XNEG_YNZN
	state.FACE_XNEG_YPZPT = FACE_XNEG_YPZPT
	state.FACE_XNEG_YNZPT = FACE_XNEG_YNZPT
	state.FACE_XNEG_YPZNT = FACE_XNEG_YPZNT
	state.FACE_XNEG_YNZNT = FACE_XNEG_YNZNT
	state.FACE_YNEG_XP = FACE_YNEG_XP
	state.FACE_YNEG_XN = FACE_YNEG_XN
	state.FACE_YNEG_ZP = FACE_YNEG_ZP
	state.FACE_YNEG_ZN = FACE_YNEG_ZN
	state.FACE_YNEG_XP_O = FACE_YNEG_XP_O
	state.FACE_YNEG_XN_O = FACE_YNEG_XN_O
	state.FACE_YNEG_ZP_O = FACE_YNEG_ZP_O
	state.FACE_YNEG_ZN_O = FACE_YNEG_ZN_O
	state.FACE_YNEG_XPZP = FACE_YNEG_XPZP
	state.FACE_YNEG_XNZP = FACE_YNEG_XNZP
	state.FACE_YNEG_XPZN = FACE_YNEG_XPZN
	state.FACE_YNEG_XNZN = FACE_YNEG_XNZN
	state.FACE_YNEG_XPZPT = FACE_YNEG_XPZPT
	state.FACE_YNEG_XNZPT = FACE_YNEG_XNZPT
	state.FACE_YNEG_XPZNT = FACE_YNEG_XPZNT
	state.FACE_YNEG_XNZNT = FACE_YNEG_XNZNT
	state.FACE_ZNEG_XP = FACE_ZNEG_XP
	state.FACE_ZNEG_XN = FACE_ZNEG_XN
	state.FACE_ZNEG_YP = FACE_ZNEG_YP
	state.FACE_ZNEG_YN = FACE_ZNEG_YN
	state.FACE_ZNEG_XP_O = FACE_ZNEG_XP_O
	state.FACE_ZNEG_XN_O = FACE_ZNEG_XN_O
	state.FACE_ZNEG_YP_O = FACE_ZNEG_YP_O
	state.FACE_ZNEG_YN_O = FACE_ZNEG_YN_O
	state.FACE_ZNEG_XPYP = FACE_ZNEG_XPYP
	state.FACE_ZNEG_XNYP = FACE_ZNEG_XNYP
	state.FACE_ZNEG_XPYN = FACE_ZNEG_XPYN
	state.FACE_ZNEG_XNYN = FACE_ZNEG_XNYN
	state.FACE_ZNEG_XPYPT = FACE_ZNEG_XPYPT
	state.FACE_ZNEG_XNYPT = FACE_ZNEG_XNYPT
	state.FACE_ZNEG_XPYNT = FACE_ZNEG_XPYNT
	state.FACE_ZNEG_XNYNT = FACE_ZNEG_XNYNT
	state.EDGE_XPYP_ZP = EDGE_XPYP_ZP
	state.EDGE_XPYP_ZN = EDGE_XPYP_ZN
	state.EDGE_XNYP_ZP = EDGE_XNYP_ZP
	state.EDGE_XNYP_ZN = EDGE_XNYP_ZN
	state.EDGE_XPYN_ZP = EDGE_XPYN_ZP
	state.EDGE_XPYN_ZN = EDGE_XPYN_ZN
	state.EDGE_XNYN_ZP = EDGE_XNYN_ZP
	state.EDGE_XNYN_ZN = EDGE_XNYN_ZN
	state.EDGE_XPZP_YP = EDGE_XPZP_YP
	state.EDGE_XPZP_YN = EDGE_XPZP_YN
	state.EDGE_XNZP_YP = EDGE_XNZP_YP
	state.EDGE_XNZP_YN = EDGE_XNZP_YN
	state.EDGE_XPZN_YP = EDGE_XPZN_YP
	state.EDGE_XPZN_YN = EDGE_XPZN_YN
	state.EDGE_XNZN_YP = EDGE_XNZN_YP
	state.EDGE_XNZN_YN = EDGE_XNZN_YN
	state.EDGE_YPZP_XP = EDGE_YPZP_XP
	state.EDGE_YPZP_XN = EDGE_YPZP_XN
	state.EDGE_YPZN_XP = EDGE_YPZN_XP
	state.EDGE_YPZN_XN = EDGE_YPZN_XN
	state.EDGE_YNZP_XP = EDGE_YNZP_XP
	state.EDGE_YNZP_XN = EDGE_YNZP_XN
	state.EDGE_YNZN_XP = EDGE_YNZN_XP
	state.EDGE_YNZN_XN = EDGE_YNZN_XN
