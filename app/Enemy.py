# -------- Enemy.py --------
# Handles all logic relating to the enemies
# ---------------------------

# Imports
import random
import Config, Vector2D
from Sprite import StaticSprite, AnimatedSprite, MovingSprite
from Event import EventListener, Event


# -------- Enemy Spore --------
class EnemySpore( AnimatedSprite ):
	looking = False
	growing = False
	move_vector = [0,0]
	speed = 10
	gravity = 4

	# Init
	def __init__( self, vector ):
		self.groups = Config.app.sprite_groups['enemy-spores'], Config.app.sprites_all
		self._layer = Config.sprite_layer_enemies

		AnimatedSprite.__init__( self, "enemies/spore.png", vector )
		x = random.randint(0, 1) + random.random()
		self.direction = random.randint(0, 1)
		if self.direction == 0: self.direction = -1
		y = 1 + random.random()
		self.move_vector = [x * self.direction, -y]

		self.AddAnimationState( "idle", 0, 2, 6 )
		self.SetAnimationState( "idle" )

		self.collide_with = [
			{
				'group': Config.app.sprite_groups['friendly-spores'],
				'module': 'Friendly',
				'event': 'CollisionEvent'
			}
		]


	# OnCollision
	def OnCollision( self, c ):

		if self.growing:
			for es in Config.app.sprite_groups['enemy-spores']:
				if es.vector[0] == self.vector[0]:
					es.kill( ) 

		if c.growing:
			for fs in Config.app.sprite_groups['friendly-spores']:
				if fs.vector[0] == c.vector[0]:
					fs.kill( )
		
		self.kill( )
		c.kill( )


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
				for spore in Config.app.sprite_groups['enemy-spores']:
					if spore != self and spore.vector[0] == self.vector[0]:
						height += 1
						spores.append(spore)
						self.vector[1] -= 8

				# If tall enough, kill spores and convert to tree
				if height > 9:
					for spore in spores:
						spore.kill( )

					EnemyTree( base )

					Config.world.SetGroundType( self.vector[0], "enemy" )


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

			self.vector[0] += (self.speed * m * -self.direction)

		self.CheckOnWater( )

		AnimatedSprite.Update( self, frame_time, ticks )




# -------- Enemy Tree --------
class EnemyTree( AnimatedSprite ):
	energy_up_rate = 1
	

	# Init
	def __init__( self, vector ):
		self.groups = Config.app.sprite_groups['enemy-trees'], Config.app.sprites_all
		self._layer = Config.sprite_layer_enemies

		AnimatedSprite.__init__( self, "enemies/tree-1.png", vector )

		self.level = 1
		self.energy = 1.0

		self.AddAnimationState( "idle", 0, 11, 6 )
		self.SetAnimationState( "idle" )

		#Config.app.em.RegisterListener( FriendlyTreePlayerCollisionListener() )


	# Update
	def Update( self, frame_time, ticks ):
		m = frame_time / 1000.0

		self.energy += (self.energy_up_rate * m)

		if self.energy > 30:
			self.level = 2
			self.ReloadSrc( "enemies/tree-2.png" )

		AnimatedSprite.Update( self, frame_time, ticks )




# -------- Enemy Flying --------
class EnemyFlying( MovingSprite ):
	max_speed 	= [300.0, 200.0] # Pixels per second
	accl 		= [10.0, 20.0] # Change per second
	dccl		= [5.0, 10.0]
	spawn_wait = 6000 # Every 6 seconds

	# Init
	def __init__( self ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['enemy-flying'], Config.app.sprites_all
		self._layer = Config.sprite_layer_enemies

		# Create as animated sprite
		MovingSprite.__init__(
			self,
			"enemies/flying-1.png",
			[Config.screen_w - 50, random.randint(50,150)]
		)

		self.cur_speed 	= [0.0, 0.0]
		self.is_accl 	= [0, 0]
		self.move_vector = [0, 0]
		self.spawning = False
		self.last_spawn = 0
		self.target = False
		self.level = 1

		self.AddAnimationState( "flying", 0, 5, 12 )
		self.SetAnimationState( "flying" )


	# Find Nearest Friendly Plant
	def FindNearestFriendlyPlant( self ):
		for plant in Config.app.sprite_groups['friendly-plants']:
			if plant.state == "eating" and plant.targeted == False:
				return plant
		return False


	# Move To Nearest Friendly Plant
	def MoveToNearestFriendlyPlant( self, frame_time ):
		m = frame_time / 1000.0
		print ""
		if self.target == False:
			self.target = self.FindNearestFriendlyPlant( )

		if self.target == False:
			# Roam
			self.is_accl[0] = 0

		else:
			if self.target.targeted and self.target.targeted_by != self:
				self.target = False
			else:
				x = self.vector[0] + (self.rect.w / 2)
				if x > self.target.vector[0]:
					self.is_accl[0] = -1
				else:
					self.is_accl[0] = 1

				if x > self.target.vector[0] - 10 and x < self.target.vector[0] + 10:
					self.target.targeted = True
					self.target.targeted_by = self

		if self.last_spawn <= 0:
			self.Spawn( )
			self.last_spawn = self.spawn_wait
		self.last_spawn -= frame_time


	# Spawn
	def Spawn( self ):
		r = self.level * 5
		for i in range( r ):
			EnemySpore( Vector2D.AddVectors(self.vector, [self.rect.w/2, 0]) )


	# Update
	def Update( self, frame_time, ticks ):
		MovingSprite.Update( self, frame_time, ticks )
		self.MoveToNearestFriendlyPlant( frame_time )




# -------- Enemy Plant --------
'''class EnemyPlant( AnimatedSprite ):
	gravity = 400.0 # fall pixels per second
	spawn_wait = 10000 # every 10 seconds
	last_spawn = 0
	energy = 1.0 # level up every 100 energy
	energy_up_rate = 5
	captured = False
	level = 1

	# Init
	def __init__( self ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['enemy-plants'], Config.app.sprites_all
		self._layer = Config.sprite_layer_enemies

		# Create as animated sprite
		AnimatedSprite.__init__(
			self,
			"enemies/plant-1.png",
			[random.randint(300, Config.screen_w - 100), 0]
		)

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
			FriendlySpore( Vector2D.AddVectors(self.vector, [self.rect.w/2, 0]) )


	# Increase Energy
	def IncreaseEnergy( self ):
		self.energy += self.energy_up_rate

		if self.energy > 100:
			self.energy = 100

			if self.level == 1:
				self.level = 2
				self.ReloadSrc( "enemies/plant-2.png" )

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

		AnimatedSprite.Update( self, frame_time, ticks )'''