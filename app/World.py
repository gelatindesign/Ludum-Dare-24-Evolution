# -------- World.py --------
# Handles all logic relating to the world
# --------------------------

# Imports
import random, math, pygame
import Config
from Sprite import StaticSprite
from Event import EventListener
from Friendly import FriendlyPlant, FriendlyTree
from Enemy import EnemyTree, EnemyFlying


# -------- World --------
class World( ):
	terrain_height = []
	terrain_angle = []
	terrain_type = []
	colour = {}

	# Init
	def __init__( self ):
		Config.app.em.RegisterListener( WorldKeyboardListener() )

		self.colour['dirt'] = (255, 200, 0)
		self.colour['water'] = (0, 200, 255)
		self.colour['friendly'] = (140, 255, 0)


	# Generate Terrain
	def GenerateTerrain( self, width ):
		rx = 50
		ry = Config.screen_h / 40
		rwater = 20 # % chance of being a water source

		# Create terrain surface
		self.terrain = pygame.Surface( (width, Config.screen_h) )
		self.terrain_height = []
		self.terrain_angle = []
		self.terrain_type = []

		w = 0
		x1 = x2 = 0
		y1 = y2 = Config.screen_h - (ry * 4)
		while x2 < width:
			x2 = random.randint( x1+10, x1+rx+1 )
			y2 = random.randint( y1-ry, y1+ry )

			if y2 > Config.screen_h - ry: y2 = Config.screen_h - ry
			if y2 < ry: y2 = ry

			if random.randint( 0, 100 ) <= rwater:
				terrain_type = 'water'
				pygame.draw.line( self.terrain, self.colour['water'], (x1, y1), (x2, y2) )
				pygame.draw.line( self.terrain, self.colour['water'], (x1, y1+1), (x2, y2+1) )
				pygame.draw.line( self.terrain, self.colour['water'], (x1, y1+2), (x2, y2+2) )
			else:
				terrain_type = 'dirt'
				pygame.draw.line( self.terrain, self.colour['dirt'], (x1, y1), (x2, y2) )

			delta_y = y1 - y2
			delta_x = x2 - x1
			angle = math.degrees( math.atan2(delta_y, delta_x) )

			xc = x1 + ((x2 - x1) / 2 )
			ym = y1 + ((y2 - y1) / 2 )
			self.terrain_type.append( (x1, x2, xc, ym, terrain_type) )

			for i in range( x1, x2 ):
				ym = y1 + ((y2 - y1) * float(float(i - x1) / float(x2 - x1)))

				self.terrain_height.append( ym )
				self.terrain_angle.append( angle )

			x1 = x2
			y1 = y2

		# Create minimap
		self.terrain_minimap = self.terrain.copy( )

		wscale = int( Config.screen_w * 0.6 )
		hscale = int( (Config.screen_h / Config.world_size) * 0.6 )

		self.terrain_minimap = pygame.transform.scale( self.terrain_minimap, (wscale , hscale) )

		# Add starting positions
		FriendlyPlant( )
		num_trees = 3
		for x1, x2, xc, ym, t in self.terrain_type:
			if t == "water":
				num_trees -= 1
				tree = FriendlyTree( [xc, ym - 80] )
				self.SetGroundType( xc, "friendly" )
				if num_trees == 0:
					break;

		num_trees = 6
		for x1, x2, xc, ym, t in reversed( self.terrain_type ):
			if t == "water":
				num_trees -= 1
				tree = EnemyTree( [xc, ym - 80] )
				tree.level = 2
				tree.energy = 30
				tree.last_spawn = 0
				self.SetGroundType( xc, "enemy" )
				if num_trees == 0:
					break;


	# Nav Map
	def NavMap( self ):
		navmap = pygame.Surface( (Config.world.terrain_minimap.get_width(), Config.world.terrain_minimap.get_height()) )
		navmap.convert_alpha( )
		navmap.set_colorkey((0,0,0))

		navmap_scale_w = float(self.terrain_minimap.get_width( )) / float(Config.screen_w * Config.world_size)
		navmap_scale_h = float(self.terrain_minimap.get_height( )) / float(Config.screen_h)

		pygame.draw.lines( navmap, (100,100,100), True, (
			(navmap_scale_w * -Config.world_offset, 0),
			((navmap_scale_w * (Config.screen_w - Config.world_offset))-1, 0),
			((navmap_scale_w * (Config.screen_w - Config.world_offset))-1, (navmap_scale_h * Config.screen_h)-1),
			(navmap_scale_w * -Config.world_offset, (navmap_scale_h * Config.screen_h)-1)
		) )

		# Add sprites
		for s in Config.app.sprites_all:
			x = s.vector[0] * navmap_scale_w
			y = s.vector[1] * navmap_scale_h
			width = 2
			height = 2

			if s.__class__.__name__ == "Player":
				colour = Config.colour_player
			elif s.__class__.__name__ == "FriendlyPlant":
				colour = Config.colour_friendly
				if s.level > 1:
					height = 4
			elif s.__class__.__name__ == "FriendlyTree":
				colour = Config.colour_friendly
				height = 8
				y += 4
				if s.level == 2:
					height = 16
					y -= 8
			elif s.__class__.__name__ == "EnergyParticle":
				colour = (255,255,255)
				height = 1
				width = 1
				y -= 1
			elif s.__class__.__name__ == "EnemyFlying":
				colour = Config.colour_enemy
				width = s.level + 1
				height = s.level + 1
			elif s.__class__.__name__ == "EnemyTree":
				colour = Config.colour_enemy
				height = 8
				y += 2
			else:
				continue

			if width < 2: width = 2
			if height < 2: height = 2

			pygame.draw.rect( navmap, colour, (
				x,
				y,
				width,
				height
			) )


		return navmap


	# Get Ground Height and Angle
	def GroundInfo( self, xlook ):
		xlook = int( xlook )
		return self.terrain_height[xlook], self.terrain_angle[xlook]


	# Get Ground Type
	def GroundType( self, xlook ):
		xlook = int( xlook )
		for x1, x2, xc, ym, t in self.terrain_type:
			if x1 <= xlook and x2 >= xlook:
				return xc, ym, t
		return 0, 0, ''
		#return self.terrain_type[xlook]


	# Set Ground Type
	def SetGroundType( self, xlook, new_type ):
		xlook = int( xlook )
		i = 0
		for x1, x2, xc, ym, t in self.terrain_type:
			if x1 <= xlook and x2 >= xlook:
				self.terrain_type[i] = x1, x2, xc, ym, new_type
				#pygame.draw.line( self.terrain, self.colour[t], (x1, y1), (x2, y2) )
				#pygame.draw.line( self.terrain, self.colour[t], (x1, y1+1), (x2, y2+1) )
				#pygame.draw.line( self.terrain, self.colour[t], (x1, y1+2), (x2, y2+2) )
			i += 1	


# -------- ResourcePoint --------
class ResourcePoint( StaticSprite ):

	# Init
	def __init__( self ):
		pass
		#StaticSprite.__init__( "world/resource-point.png", [0,0] )


# -------- World Keyboard Listener --------
class WorldKeyboardListener( EventListener ):
	# Notify
	def Notify( self, event ):
		if event.name == "Pygame Event":
			if event.data.type == pygame.KEYDOWN:
				if event.data.key == pygame.K_t:
					Config.world.GenerateTerrain( Config.screen_w * Config.world_size )
				elif event.data.key == pygame.K_e:
					EnemyFlying( [400, Config.screen_h - 50] )
				elif event.data.key == pygame.K_f:
					FriendlyPlant( )