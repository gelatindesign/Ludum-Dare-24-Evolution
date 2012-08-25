# -------- World.py --------
# Handles all logic relating to the world
# --------------------------

# Imports
import random, math, pygame
import Config
from Sprite import StaticSprite
from Event import EventListener
from Friendly import FriendlyBug


# -------- World --------
class World( ):
	terrain_height = []
	terrain_angle = []

	# Init
	def __init__( self ):
		Config.app.em.RegisterListener( WorldKeyboardListener() )


	# Generate Terrain
	def GenerateTerrain( self, width ):
		rx = 50
		ry = Config.screen_h / 20

		# Create terrain surface
		self.terrain = pygame.Surface( (width, Config.screen_h) )
		self.terrain_height = []
		self.terrain_angle = []

		colour = (160, 255, 160)

		w = 0
		x1 = x2 = 0
		y1 = y2 = Config.screen_h - (ry * 4)
		while x2 < width:
			x2 = random.randint( x1+1, x1+rx+1 )
			y2 = random.randint( y1-ry, y1+ry )

			if y2 > Config.screen_h - ry: y2 = Config.screen_h - ry

			pygame.draw.line( self.terrain, colour, (x1, y1), (x2, y2) )

			delta_y = y1 - y2
			delta_x = x2 - x1
			angle = math.degrees( math.atan2(delta_y, delta_x) )

			for i in range( x1, x2 ):
				#ym = y2 - (y2-y1) / (float((x2 - x1)) / float(i))

				#ym = y1 + ((y2 - y1) / (float(x2 - x1) / float(x2 - i))) # * ((x2 - i) / (x2 - x1))
				#print (float(x2 - x1) / float(x2 - i))

				ym = y1 + ((y2 - y1) * float(float(i - x1) / float(x2 - x1)))

				self.terrain_height.append( ym )
				self.terrain_angle.append( angle )

			x1 = x2
			y1 = y2

		#self.terrain_array = pygame.surfarray.array2d( self.terrain )
		#print self.terrain_height
		for i in range(4):
			FriendlyBug( )


	# Get Average World Height
	def GroundInfo( self, xlook ):
		'''
		#print "xlook", xlook
		for x in self.terrain_array:
			#print "xfind", x
			if xlook < x:
				y = self.terrain_array[x]
				#print "yfind", x, y
				return y
		'''
		return self.terrain_height[xlook], self.terrain_angle[xlook]


# -------- ResourcePoint --------
class ResourcePoint( StaticSprite ):

	# Init
	def __init__( self ):
		pass


# -------- World Keyboard Listener --------
class WorldKeyboardListener( EventListener ):
	# Notify
	def Notify( self, event ):
		if event.name == "Pygame Event":
			if event.data.type == pygame.KEYDOWN:
				if event.data.key == pygame.K_t:
					Config.world.GenerateTerrain( Config.screen_w * Config.world_size )