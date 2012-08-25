# -------- Player.py --------
# Handles all logic relating to the Player
# ---------------------------

# Imports
import pygame, Config
import Vector2D
from Event import EventManager, EventListener
from Sprite import StaticSprite, AnimatedSprite

# -------- Player --------
class Player( AnimatedSprite ):
	control_FIRE_PRIMARY = 1 # Mouse left
	control_FIRE_SECONDARY = 3 # Mouse right

	speed = 1 # Pixels per tick
	
	# Init
	def __init__( self ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['player'], Config.app.sprites_all
		self._layer = Config.sprite_layer_player

		# Create as animated sprite
		AnimatedSprite.__init__(
			self,
			"player/player.png",
			[20, 20], #[0, Config.screen_h / 2]
			False
		)

		self.AddAnimationState( "moving", 0, 7, 6 )
		self.SetAnimationState( "moving" )

		# Register listeners
		Config.app.em.RegisterListener( MouseListener() )
		Config.app.em.RegisterListener( KeyboardListener() )

		Config.player = self


	# Move
	def Move( self, event ):
		if event.key == self.control_MOVE_UP:
			move_vector = Vector2D.UP
		elif event.key == self.control_MOVE_RIGHT:
			move_vector = Vector2D.RIGHT
		elif event.key == self.control_MOVE_DOWN:
			move_vector = Vector2D.DOWN
		elif event.key == self.control_MOVE_LEFT:
			move_vector = Vector2D.LEFT

		self.vector = Vector2D.AddVectors( self.vector, move_vector )


	# Fire Energy
	def FireEnergy( self, target_vector ):
		e = EnergyParticle( self.vector, target_vector )


	# Fire Pulse
	def FirePulse( self ):
		pass


	# Control Mouse Down
	def ControlMouseDown( self, event ):
		if event.button == self.control_FIRE_PRIMARY:
			target_vector = [ event.pos[0], event.pos[1] ]
			self.FireEnergy( target_vector )

		elif event.button == self.control_FIRE_SECONDARY:
			self.FirePulse( )


	# Control Mouse Up
	def ControlMouseUp( self, event ):
		pass


	# Control Mouse Motion
	def ControlMouseMotion( self, event ):
		pass


# -------- EnergyParticle --------
class EnergyParticle( StaticSprite ):
	pass


# -------- Keyboard Listener --------
class KeyboardListener( EventListener ):
	pass


# -------- Mouse Listener ---------
class MouseListener( EventListener ):

	# Init
	def Notify( self, event ):
		if event.name == "Pygame Event":
			if event.data.type == pygame.MOUSEBUTTONDOWN:
				Config.player.ControlMouseDown( event.data )

			elif event.data.type == pygame.MOUSEBUTTONUP:
				Config.player.ControlMouseUp( event.data )

			elif event.data.type == pygame.MOUSEMOTION:
				Config.player.ControlMouseMotion( event.data )