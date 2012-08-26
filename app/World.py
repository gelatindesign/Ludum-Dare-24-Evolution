# -------- World.py --------
# Handles all logic relating to the world
# --------------------------

# Imports
import random, math, pygame
import Config
from Sprite import StaticSprite
from Event import EventListener
from Friendly import FriendlyPlant


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
		ry = Config.screen_h / 20
		rwater = 10 # % chance of being a water source

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

		for i in range(1):
			FriendlyPlant( )

		ResourcePoint( )


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