# -------- Friendly.py --------
# Handles all logic relating to the friendlies
# -----------------------------

# Imports
import random
import Config, Vector2D
from Sprite import StaticSprite, AnimatedSprite, MovingSprite
from Event import EventListener

# -------- Friendly Spore --------
class FriendlySpore( AnimatedSprite ):
	looking = False
	move_vector = [0,0]
	speed = 10

	# Init
	def __init__( self, vector ):
		self.groups = Config.app.sprite_groups['friendly-spores'], Config.app.sprites_all
		self._layer = Config.sprite_layer_friendlies

		AnimatedSprite.__init__( self, "friendlies/spore.png", vector )
		x = random.randint(1, 4)
		self.direction = random.randint(0, 1)
		if self.direction == 0: self.direction = -1
		y = random.randint(10, 30)
		self.move_vector = [x * self.direction, -y]

		self.AddAnimationState( "idle", 0, 2, 6 )
		self.SetAnimationState( "idle" )

	# Update
	def Update( self, frame_time, ticks ):
		m = frame_time / 1000.0

		# Get ground height
		ground_height, ground_angle = Config.world.GroundInfo( self.vector[0] )

		if self.looking == False:
			if self.vector[1] < ground_height - 6:
				self.move_vector[1] += 1
				self.vector = Vector2D.AddVectors( self.vector, self.move_vector )
			else:
				self.looking = True

		if self.looking == True:
			if self.vector[1] < ground_height - 6:
				self.vector[1] += 1
			elif self.vector[1] > ground_height - 6:
				self.vector[1] -= 1

			self.vector[0] += self.speed * m * self.direction

		AnimatedSprite.Update( self, frame_time, ticks )



# -------- Friendly Plant --------
class FriendlyPlant( AnimatedSprite ):
	gravity = 400.0 # fall pixels per second
	spawn_wait = 10000 # every 10 seconds
	last_spawn = 0
	energy = 1.0 # level up every 100 energy
	energy_up_rate = 5 # every second

	# Init
	def __init__( self ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['friendly-plants'], Config.app.sprites_all
		self._layer = Config.sprite_layer_friendlies

		# Create as animated sprite
		AnimatedSprite.__init__(
			self,
			"friendlies/friendly-bug-1b.png",
			[random.randint(100, Config.screen_w - 100), 0]
		)

		self.AddAnimationState( "eating", 0, 3, 4 )
		self.AddAnimationState( "jumping", 4, 9, 4 )
		self.AddAnimationState( "falling", 10, 10, 1 )
		self.AddAnimationState( "landing", 11, 15, 4 )
		self.SetAnimationState( "falling" )

	# Spawn
	def Spawn( self ):
		self.last_spawn = self.spawn_wait

		# Create a friendly spore
		r = random.randint( 1 + int(self.energy / 20), 1 + int(self.energy / 10) )
		for i in range( r ):
			FriendlySpore( self.vector )

	# Update
	def Update( self, frame_time, ticks ):
		m = frame_time / 1000.0

		# Set energy level
		self.energy += (self.energy_up_rate * m)

		# Get ground height at centre x of bug
		ground_height, ground_angle = Config.world.GroundInfo( self.vector[0] + (self.rect.w/2) )

		# Get bottom of bug
		#self.image_angle = ground_angle
		bottom = self.vector[1] + self.rect.h

		#print bottom, ground

		# Check if bug is above the ground
		if bottom < ground_height - 1:
			self.vector = Vector2D.AddVectors( self.vector, [0, self.gravity * m] )

		elif bottom > ground_height:
			self.vector = Vector2D.SubtractVectors( self.vector, [0, 1] )
		else:
			self.SetAnimationState( "eating" )

			if self.last_spawn <= 0:
				self.Spawn( )
			else:
				self.last_spawn -= frame_time

		AnimatedSprite.Update( self, frame_time, ticks )


# -------- Friendly Plant Energy Collision --------
class FriendlyPlantEnergyCollisionEvent( Event ):
	name = "Friendly Plant Energy Collision Event"

class FriendlyPlantEnergyCollisionListener( EventListener ):
	# Notify
	def Notify( event ):
		if event.name == "Friendly Plant Energy Collision Event":
			pass