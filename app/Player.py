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
	control_MOVE_UP = pygame.K_w
	control_MOVE_RIGHT = pygame.K_d
	control_MOVE_DOWN = pygame.K_s
	control_MOVE_LEFT = pygame.K_a

	max_speed 	= [400.0, 200.0] # Pixels per second
	cur_speed 	= [0.0, 0.0]
	accl 		= [20.0, 30.0] # Change per second
	dccl		= [10.0, 20.0]
	is_accl 	= [0, 0]

	move_vector = [0, 0]
	
	# Init
	def __init__( self ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['player'], Config.app.sprites_all
		self._layer = Config.sprite_layer_player

		# Create as animated sprite
		AnimatedSprite.__init__(
			self,
			"player/player.png",
			[20, Config.screen_h / 2],
			False
		)

		self.AddAnimationState( "moving", 0, 7, 6 )
		self.SetAnimationState( "moving" )

		# Register listeners
		Config.app.em.RegisterListener( MouseListener() )
		Config.app.em.RegisterListener( KeyboardListener() )

		Config.player = self


	# Move
	def Move( self, frame_time ):
		m = frame_time / 1000.0

		for i in range( 2 ):
			if self.is_accl[i] != 0:
				self.cur_speed[i] += self.accl[i] * self.is_accl[i]

				if self.cur_speed[i] > self.max_speed[i]: self.cur_speed[i] = self.max_speed[i]
				if self.cur_speed[i] < -self.max_speed[i]: self.cur_speed[i] = -self.max_speed[i]

			else:
				if self.cur_speed[i] > 0:
					self.cur_speed[i] -= self.dccl[i]
					if self.cur_speed[i] < self.dccl[i]: self.cur_speed[i] = 0.0
				elif self.cur_speed[i] < 0:
					self.cur_speed[i] += self.dccl[i]
					if self.cur_speed[i] > self.dccl[i]: self.cur_speed[i] = 0.0

			self.move_vector[i] = self.cur_speed[i] * m

		self.vector = Vector2D.AddVectors( self.vector, self.move_vector )


	# Fire Energy
	def FireEnergy( self, target_vector ):
		e = EnergyParticle( self.vector, target_vector )


	# Fire Pulse
	def FirePulse( self ):
		pass


	# Update
	def Update( self, frame_time, ticks ):
		AnimatedSprite.Update( self, frame_time, ticks )
		self.Move( frame_time )


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


	# Control Keyboard Down
	def ControlKeyDown( self, event ):
		if event.key == self.control_MOVE_UP:
			self.is_accl[1] = -1
		elif event.key == self.control_MOVE_RIGHT:
			self.is_accl[0] = 1
		elif event.key == self.control_MOVE_DOWN:
			self.is_accl[1] = 1
		elif event.key == self.control_MOVE_LEFT:
			self.is_accl[0] = -1


	# Control Keyboard Up
	def ControlKeyUp( self, event ):
		if event.key == self.control_MOVE_UP:
			if self.is_accl[1] == -1:
				self.is_accl[1] = 0
		elif event.key == self.control_MOVE_RIGHT:
			if self.is_accl[0] == 1:
				self.is_accl[0] = 0
		elif event.key == self.control_MOVE_DOWN:
			if self.is_accl[1] == 1:
				self.is_accl[1] = 0
		elif event.key == self.control_MOVE_LEFT:
			if self.is_accl[0] == -1:
				self.is_accl[0] = 0



# -------- EnergyParticle --------
class EnergyParticle( StaticSprite ):
	pass


# -------- Keyboard Listener --------
class KeyboardListener( EventListener ):
	# Notify
	def Notify( self, event ):
		if event.name == "Pygame Event":
			if event.data.type == pygame.KEYDOWN:
				Config.player.ControlKeyDown( event.data )

			elif event.data.type == pygame.KEYUP:
				Config.player.ControlKeyUp( event.data )


# -------- Mouse Listener ---------
class MouseListener( EventListener ):
	# Notify
	def Notify( self, event ):
		if event.name == "Pygame Event":
			if event.data.type == pygame.MOUSEBUTTONDOWN:
				Config.player.ControlMouseDown( event.data )

			elif event.data.type == pygame.MOUSEBUTTONUP:
				Config.player.ControlMouseUp( event.data )

			elif event.data.type == pygame.MOUSEMOTION:
				Config.player.ControlMouseMotion( event.data )