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

material( 'mc_stone' )
material( 'mc_cobble' )
material( 'mc_admin' )
material( 'mc_dirt' )
material( 'mc_plank' )
material( 'mc_gravel' )
material( 'mc_gold' )
material( 'mc_iron' )
material( 'mc_coal' )
material( 'mc_diamond' )
material( 'mc_redstone' )
material( 'mc_glass' )
material( 'mc_chest' )
material( 'mc_craft' )
material( 'mc_furnace' )
material( 'mc_lapis' )
material( 'mc_lamp' )
material( 'mc_wood' )
material( 'mc_brick' )
material( 'mc_obsidian' )
material( 'mc_nether' )
material( 'mc_face' )
material( 'mc_light' )
material( 'mc_sand' )
material( 'mc_tnt' )
material( 'mc_books' )
material( 'mc_mossy' )
material( 'mc_disp' )
material( 'mc_sponge' )
material( 'mc_ice' )
material( 'mc_note' )
material( 'mc_myc' )
material( 'mc_soil' )
material( 'mc_wall' )
material( 'mc_wallmoss' )
material( 'mc_wallcrack' )
material( 'mc_pump' )
material( 'mc_cake' )

material( 'black' )

material( 'dala_coolinglava' )
material( 'dala_whitecloud' )
