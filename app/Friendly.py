# -------- Friendly.py --------
# Handles all logic relating to the friendlies
# -----------------------------

# Imports
import random
import Config, Vector2D
from Sprite import StaticSprite, AnimatedSprite, MovingSprite
from Event import EventListener, Event

# -------- Friendly Spore --------
class FriendlySpore( AnimatedSprite ):
	speed = 10
	gravity = 1

	# Init
	def __init__( self, vector ):
		self.groups = Config.app.sprite_groups['friendly-spores'], Config.app.sprites_all
		self._layer = Config.sprite_layer_friendlies

		AnimatedSprite.__init__( self, "friendlies/spore.png", vector )

		self.looking = False
		self.growing = False
		self.move_vector = [0,0]

		x = random.random()
		self.direction = random.randint(0, 1)
		if self.direction == 0: self.direction = -1
		y = random.randint(1, 3) + random.random()
		self.move_vector = [x * self.direction, -y]

		self.AddAnimationState( "idle", 0, 2, 6 )
		self.SetAnimationState( "idle" )


	# Check On Water
	def CheckOnWater( self ):
		if self.looking == True and self.growing == False:
			xc, ym, terrain = Config.world.GroundType( self.vector[0] )
			if terrain == 'water':
				self.growing = True

				# Move to center of water hole
				self.vector[0] = xc
				self.vector[1] = ym

				# Stack on top of other spores
				height = 0
				spores = [self]
				base = self.vector
				for spore in Config.app.sprite_groups['friendly-spores']:
					if spore != self and spore.vector[0] == self.vector[0]:
						height += 1
						spores.append(spore)
						self.vector[1] -= 8

				# If tall enough, kill spores and convert to tree
				if height > 9:
					for spore in spores:
						spore.kill( )

					FriendlyTree( base )

					Config.world.SetGroundType( self.vector[0], "friendly" )


	# Update
	def Update( self, frame_time, ticks ):
		m = frame_time / 1000.0

		# Get ground height
		ground_height, ground_angle = Config.world.GroundInfo( self.vector[0] )

		if self.growing == True:
			# Found water and growing
			pass

		elif self.looking == False:
			# In the air
			if self.vector[1] < ground_height - 6:
				self.move_vector[1] += self.gravity * m
				self.vector = Vector2D.AddVectors( self.vector, self.move_vector )
			else:
				self.looking = True

		elif self.looking == True:
			# Moving on the ground
			if self.vector[1] < ground_height - 6:
				self.vector[1] += 1
			elif self.vector[1] > ground_height - 6:
				self.vector[1] -= 1

			self.vector[0] += (self.speed * m * self.direction)

		self.CheckOnWater( )

		AnimatedSprite.Update( self, frame_time, ticks )



# -------- Friendly Tree --------
class FriendlyTree( AnimatedSprite ):
	energy_up_rate = 1

	# Init
	def __init__( self, vector ):
		self.groups = Config.app.sprite_groups['friendly-trees'], Config.app.sprites_all
		self._layer = Config.sprite_layer_friendlies

		AnimatedSprite.__init__( self, "friendlies/tree-1.png", vector )

		self.energy = 1.0
		self.level = 1

		self.AddAnimationState( "idle", 0, 11, 6 )
		self.SetAnimationState( "idle" )

		Config.app.em.RegisterListener( FriendlyTreePlayerCollisionListener() )


	# CapturedByPlayer
	def CapturedByPlayer( self ):
		if self.level == 2 and Config.player.has_captured == False:
			Config.world.SetGroundType( self.vector[0], "water" )
			self.kill( )

			Config.player.captured_plant = FriendlyPlant( )
			Config.player.captured_plant.vector = Vector2D.AddVectors( Config.player.vector, [5, 20] )
			Config.player.captured_plant.captured = True

			Config.player.has_captured = True


	# Update
	def Update( self, frame_time, ticks ):
		m = frame_time / 1000.0

		self.energy += (self.energy_up_rate * m)

		if self.energy > 30:
			self.level = 2
			self.ReloadSrc( "friendlies/tree-2.png" )

		AnimatedSprite.Update( self, frame_time, ticks )



# -------- Friendly Plant --------
class FriendlyPlant( AnimatedSprite ):
	gravity = 400.0 # fall pixels per second
	spawn_wait = 10000 # every 10 seconds
	energy_up_rate = 5
	

	# Init
	def __init__( self ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['friendly-plants'], Config.app.sprites_all
		self._layer = Config.sprite_layer_friendlies

		# Create as animated sprite
		AnimatedSprite.__init__(
			self,
			"friendlies/plant-1.png",
			[random.randint(100, random.randint(300, Config.screen_w - 300)), 0]
		)

		self.last_spawn = 0
		self.energy = 1.0 # level up every 100 energy
		self.level = 1

		self.captured = False

		self.targeted = False
		self.targeted_by = None

		self.AddAnimationState( "eating", 0, 3, 4 )
		#self.AddAnimationState( "jumping", 4, 9, 4 )
		#self.AddAnimationState( "falling", 10, 10, 1 )
		#self.AddAnimationState( "landing", 11, 15, 4 )
		self.SetAnimationState( "eating" )

		Config.app.em.RegisterListener( FriendlyPlantEnergyCollisionListener() )

	# Spawn
	def Spawn( self ):
		self.last_spawn = self.spawn_wait

		# Create a friendly spore
		if self.level == 1:
			r = 1
		else:
			r = random.randint( 1 + int(self.energy / 20), 1 + int(self.energy / 10) )

		for i in range( r ):
			FriendlySpore( Vector2D.AddVectors(self.GetDrawPos( ), [self.rect.w/2, 0]) )


	# Increase Energy
	def IncreaseEnergy( self ):
		self.energy += self.energy_up_rate

		if self.energy > 100:
			self.energy = 100

			if self.level == 1:
				self.level = 2
				self.ReloadSrc( "friendlies/plant-2.png" )

	# Update
	def Update( self, frame_time, ticks ):
		m = frame_time / 1000.0

		if self.captured:
			self.vector = Vector2D.AddVectors( Config.player.vector, [5, 20] )

		else:

			# Set energy level
			#self.energy += (self.energy_up_rate * m)

			# Get ground height at centre x of bug
			ground_height, ground_angle = Config.world.GroundInfo( self.vector[0] + (self.rect.w/2) )

			# Get bottom of bug
			#self.image_angle = ground_angle
			bottom = self.vector[1] + self.rect.h

			# Check if bug is above the ground
			if bottom < ground_height - 1:
				self.vector = Vector2D.AddVectors( self.vector, [0, self.gravity * m] )

			elif bottom > ground_height:
				self.vector = Vector2D.SubtractVectors( self.vector, [0, 1] )
			else:
				self.SetAnimationState( "eating" )

				if self.last_spawn <= 0:
					self.Spawn( )
					self.energy += self.energy_up_rate
				else:
					self.last_spawn -= frame_time

		AnimatedSprite.Update( self, frame_time, ticks )




# -------- Friendly Plant Energy Collision Listener --------
class FriendlyPlantEnergyCollisionListener( EventListener ):
	# Notify
	def Notify( self, event ):
		if event.name == "Friendly Plant Energy Collision Event":
			event.data.IncreaseEnergy( )


# -------- Friendly Tree Player Collision Listener --------
class FriendlyTreePlayerCollisionListener( EventListener ):
	# Notify
	def Notify( self, event ):
		if event.name == "Friendly Tree Player Collision Event":
			event.data.CapturedByPlayer( )