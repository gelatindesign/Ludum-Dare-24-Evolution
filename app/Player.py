# -------- Player.py --------
# Handles all logic relating to the Player
# ---------------------------

# Imports
import pygame, Config
import Vector2D
from Event import EventManager, EventListener
from Sprite import StaticSprite, MovingSprite

# -------- Player --------
class Player( MovingSprite ):
	control_FIRE_PRIMARY = 1 # Mouse left
	control_FIRE_SECONDARY = 3 # Mouse right
	control_MOVE_UP = pygame.K_w
	control_MOVE_RIGHT = pygame.K_d
	control_MOVE_DOWN = pygame.K_s
	control_MOVE_LEFT = pygame.K_a

	max_speed 	= [600.0, 400.0] # Pixels per second
	cur_speed 	= [0.0, 0.0]
	accl 		= [10.0, 20.0] # Change per second
	dccl		= [5.0, 10.0]
	is_accl 	= [0, 0]

	move_vector = [0, 0]

	energy_flip = 0
	energy_rate = 8 # per second
	is_firing_energy = False
	has_fired_energy = False
	
	# Init
	def __init__( self ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['player'], Config.app.sprites_all
		self._layer = Config.sprite_layer_player

		# Create as animated sprite
		MovingSprite.__init__(
			self,
			"player/player.png",
			[20, Config.screen_h / 2]
		)

		self.AddAnimationState( "moving", 0, 7, 6 )
		self.SetAnimationState( "moving" )

		# Register listeners
		Config.app.em.RegisterListener( PlayerMouseListener() )
		Config.app.em.RegisterListener( PlayerKeyboardListener() )

		self.collide_with = [
			{
				'group': Config.app.sprite_groups['friendly-trees'],
				'module': 'Friendly',
				'event': 'FriendlyTreePlayerCollisionEvent'
			},
		]

		Config.player = self


	# Fire Energy
	def FireEnergy( self ):
		if self.cur_speed[0] >= 0:
			direction = 1
		else:
			direction = -1

		# Flip which gun fires the particle
		self.energy_flip = 1 - self.energy_flip
		if (self.energy_flip):
			vector = Vector2D.AddVectors( self.vector, [direction * 20, 9] )
		else:
			vector = Vector2D.AddVectors( self.vector, [direction * 20, 19] )

		# Create energy particle
		EnergyParticle( vector, direction )


	# Fire Pulse
	def FirePulse( self ):
		pass

	
	# Update
	def Update( self, frame_time, ticks ):
		if self.is_firing_energy:
			if self.has_fired_energy <= 0:
				self.FireEnergy( )
				self.has_fired_energy = 1000 / self.energy_rate

		if self.has_fired_energy > 0:
			self.has_fired_energy -= frame_time

		MovingSprite.Update( self, frame_time, ticks )


	# Control Mouse Down
	def ControlMouseDown( self, event ):
		if event.button == self.control_FIRE_PRIMARY:
			self.is_firing_energy = True

		elif event.button == self.control_FIRE_SECONDARY:
			self.FirePulse( )


	# Control Mouse Up
	def ControlMouseUp( self, event ):
		if event.button == self.control_FIRE_PRIMARY:
			self.is_firing_energy = False


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
	max_speed = [1000.0, 0.0]
	

	# Init
	def __init__( self, vector, direction ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['energy-particles'], Config.app.sprites_all
		self._layer = Config.sprite_layer_player

		StaticSprite.__init__( self, "player/energy-particle.png", vector )

		self.direction = direction

		self.collide_with = [
			{
				'group': Config.app.sprite_groups['friendly-plants'],
				'module': 'Friendly',
				'event': 'FriendlyPlantEnergyCollisionEvent'
			},
			{
				'group': Config.app.sprite_groups['enemy-bugs'],
				'module': 'Enemy',
				'event': 'EnemyBugEnergyCollisionEvent'
			}
		]


	# Update
	def Update( self, frame_time, ticks ):
		m = (frame_time / 1000.0) * self.direction

		self.move_vector = Vector2D.MultiplyVectors( self.max_speed, [m, 0] )
		self.vector = Vector2D.AddVectors( self.vector, self.move_vector )

		StaticSprite.Update( self, frame_time, ticks )

		if self.vector[0] > Config.screen_w * Config.world_size or self.vector[0] < 0:
			self.kill( )


	# On Collision
	def OnCollision( self ):
		self.kill( )


# -------- Player Keyboard Listener --------
class PlayerKeyboardListener( EventListener ):
	# Notify
	def Notify( self, event ):
		if event.name == "Pygame Event":
			if event.data.type == pygame.KEYDOWN:
				Config.player.ControlKeyDown( event.data )

			elif event.data.type == pygame.KEYUP:
				Config.player.ControlKeyUp( event.data )


# -------- Player Mouse Listener ---------
class PlayerMouseListener( EventListener ):
	# Notify
	def Notify( self, event ):
		if event.name == "Pygame Event":
			if event.data.type == pygame.MOUSEBUTTONDOWN:
				Config.player.ControlMouseDown( event.data )

			elif event.data.type == pygame.MOUSEBUTTONUP:
				Config.player.ControlMouseUp( event.data )

			elif event.data.type == pygame.MOUSEMOTION:
				Config.player.ControlMouseMotion( event.data )