# -------- App.py -----------
# Handles all general application logic, such as rendering either the game or
# menu and capturing & pushing events
# ------------------------

# Imports
import pygame, Config
from Event import EventManager, EventListener

# -------- App -----------
class App( ):
	running = False
	prefs = None

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


	# Tick
	# Process a single tick
	#
	# @param object self
	# @return object self
	
	def Tick( self ):
		pass


# -------- App Listener -----------
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