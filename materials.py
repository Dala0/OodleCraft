from pyglet import image

icons = {}

loadpink = False
import sys
if len( sys.argv ) > 1:
	if sys.argv[1] == 'fizzy':
		loadpink = True
		
dirt = 0
dads = 0
stuff = 0;

white = (1,1,1)
black = (0,0,0)

if loadpink:
	dirt = image.load('sprites/pinkdirt.png')
	dads = image.load('sprites/pinkdads.png')
	stuff = image.load('sprites/pinkstuff.png')
else:
	dirt = image.load('sprites/dirt.png')
	dads = image.load('sprites/dads.png')
	stuff = image.load('sprites/stuff.png')

def get_sub_icon( asset, x, y, colortoreplacewithalpha = None ):
	icon = sub = asset.get_region(16*x,16*y,16,16)
	return icon
	
def asset( name, source, x, y, colortoreplacewithalpha = None ):
	global icons
	icons[ name ] = get_sub_icon( source, x,7-y, colortoreplacewithalpha )
	
asset( 'black', stuff, 2,0, white )
asset( 'person', stuff, 1,2, white )
asset( 'coal', stuff, 2,1, white )
asset( 'sapling', stuff, 1,0, white )
asset( 'chest', stuff, 0,5, white )
asset( 'oven', stuff, 1,4, white )
asset( 'bench', stuff, 2,5, white )
asset( 'llama', dirt, 1,3, white )
asset( 'stone', dirt, 1,5 )
asset( 'cave', dirt, 2,5 )
asset( 'goldore', dirt, 3,1 )
asset( 'gold', dirt, 4,2 )
asset( 'iron', dirt, 3,3 )
asset( 'ironore', dirt, 7,3 )
asset( 'diamondore', dirt, 6,4 )
asset( 'diamond', dirt, 7,5 )
asset( 'wall', dirt, 0,2 )
asset( 'monster', dirt, 5,5, white )
asset( 'sky', stuff, 0,3 )
asset( 'grass', dirt, 4,6 )
asset( 'dirt', dirt, 0,0 )
asset( 'sand', dirt, 2,2 )
asset( 'lava', dirt, 0,7 )
asset( 'lava0', dirt, 0,7 )
asset( 'lava1', dirt, 1,7 )
asset( 'lava2', dirt, 2,7 )
asset( 'water', stuff, 0,0 )
asset( 'water0', stuff, 0,0 )
asset( 'water1', stuff, 0,1 )
asset( 'water2', stuff, 0,2 )
asset( 'wood', dirt, 2,0 )
asset( 'leaf', dirt, 5,1 )
asset( 'axe', dirt, 0,4 )
asset( 'bow', dirt, 0,6 )
asset( 'arrow', dirt, 6,6 )

asset( 'mansidel', dads, 2,3, white )
asset( 'mansider', dads, 0,3, white )
asset( 'crack0', dads, 7,0, white )
asset( 'crack1', dads, 7,1, white )
asset( 'crack2', dads, 7,2, white )
asset( 'crack3', dads, 7,3, white )
asset( 'crack4', dads, 7,4, white )
asset( 'crack5', dads, 7,5, white )
asset( 'crack6', dads, 7,6, white )
asset( 'crack7', dads, 7,7, white )
asset( 'crack8', dads, 6,0, white )
asset( 'crack9', dads, 6,1, white )
asset( 'crack10', dads, 6,2, white )
asset( 'crack11', dads, 6,3, white )
asset( 'crack12', dads, 6,4, white )
asset( 'crack13', dads, 6,5, white )
asset( 'crack14', dads, 6,6, white )
asset( 'crack15', dads, 6,7, white )
asset( 'light', dads, 0,7 )
asset( 'cursor', dads, 0,0 )
