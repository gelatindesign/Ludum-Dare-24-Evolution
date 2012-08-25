# -------- App.py --------
# Handles all general application logic, such as rendering either the game or
# menu and capturing & pushing events
# ------------------------

# Imports
import pygame, Config
from Event import EventManager, EventListener
from Player import Player

# -------- App --------
class App( ):
	running = False
	mode = 'Game' # temp, default to  menu
	prefs = None
	sprite_groups = {}


	# Init
	# Create the app object and set it to running
	# 
	# @param object self
	# @return object self

	def __init__( self ):
		# Set app to running
		self.running = True

		# Create the event manager
		self.em = EventManager( )

		self.em.RegisterListener( AppListener() )

		# Load the preferences
		prefs_file = open( "preferences.txt", "r" )
		prefs_s = prefs_file.read( ).split( "\n" )
		self.prefs = { }
		for p in prefs_s:
			pref = p.split( " " )
			self.prefs[ pref[0] ] = pref[1]

		# Set screen width & height
		Config.screen_w = int( self.prefs["screen_width"] )
		Config.screen_h = int( self.prefs["screen_height"] )


	# Load Game
	# Bring in all the required assets for the game and initialise starting
	# objects
	#
	# @return None

	def LoadGame( self ):
		# Create the sprite groups and layers
		self.sprite_groups['player'] = pygame.sprite.Group( )
		self.sprites_all = pygame.sprite.LayeredUpdates( )

		# Create the player
		p = Player( )


	# Tick
	# Process a single tick
	#
	# @param object self
	# @return object self
	
	def Tick( self, frame_time ):
		if self.mode == "Game":
			self.TickGame( frame_time )
		else:
			self.TickMenu( frame_time )


	def TickGame( self, frame_time ):
		Config.screen.fill( (0,0,0) )

		for s in self.sprites_all:
			s.Update( int(frame_time), int(pygame.time.get_ticks()) )

		rects = self.sprites_all.draw( Config.screen )
		#pygame.display.update( rects )
		pygame.display.flip( )


	def TickMenu( self ):
		pass


# -------- App Listener --------
class AppListener( EventListener ):

	# Init
	def __init__( self ):
		pass

	# Notify
	def Notify( self, event ):
		if event.name == "Pygame Event":
			if event.data.type == pygame.QUIT:
				Config.app.running = False
				print "Exiting app..."