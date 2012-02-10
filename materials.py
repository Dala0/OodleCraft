#material types

MAX_ID = 0 # IDs actually start from 1, 0 is assumed to be empty.
lookup = {}
reverselookup = {}
def material( m ):
	global MAX_ID
	MAX_ID = MAX_ID + 1
	lookup[ MAX_ID ] = m
	reverselookup[ m ] = MAX_ID
	
def addmaterials( struct ):
	struct.MAX_ID = MAX_ID
	struct.lookup = lookup
	struct.reverselookup = reverselookup
	
material( 'stone' )
material( 'dirt' )
material( 'grass' )
material( 'coal' )
material( 'cave' )
material( 'goldore' )
material( 'gold' )
material( 'iron' )
material( 'ironore' )
material( 'diamondore' )
material( 'diamond' )
material( 'wall' )
material( 'sand' )
material( 'lava' )
material( 'water' )
material( 'wood' )
material( 'leaf' )

material( 'sapling' )

material( 'chest' )
material( 'oven' )
material( 'bench' )

material( 'lava0' )
material( 'lava1' )
material( 'lava2' )
material( 'water0' )
material( 'water1' )
material( 'water2' )

