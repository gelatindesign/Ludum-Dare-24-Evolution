# -------- Enemy.py --------
# Handles all logic relating to the enemies
# ---------------------------

# Imports
import random, pygame.mixer
import Config, Vector2D
from Sprite import StaticSprite, AnimatedSprite, MovingSprite
from Event import EventListener, Event

# Load sounds
pygame.mixer.init( )
sound_die = pygame.mixer.Sound( "sounds/enemy-die.wav" )


# -------- Enemy Spore --------
class EnemySpore( AnimatedSprite ):
	looking = False
	growing = False
	move_vector = [0,0]
	speed = 40
	gravity = 4
	health = 20.0

	# Init
	def __init__( self, vector ):
		self.groups = Config.app.sprite_groups['enemy-spores'], Config.app.sprites_all
		self._layer = Config.sprite_layer_enemies

		AnimatedSprite.__init__( self, "enemies/spore.png", vector )

		self.AddAnimationState( "idle", 0, 2, 6 )
		self.SetAnimationState( "idle" )

		x = random.randint(0, 1) + random.random()
		self.direction = random.randint(0, 1)
		if self.direction == 0: self.direction = -1
		y = 1 + random.random()
		self.move_vector = [x * self.direction, -y]

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

		if self.vector[0] <= 0:
			self.direction = -self.direction
			self.vector[0] = 0
		elif self.vector[0] >= Config.screen_w * Config.world_size:
			self.direction = -self.direction
			self.vector[0] = Config.screen_w * Config.world_size 

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

			self.health -= m
			if self.health <= 0:
				self.kill( )

		self.CheckOnWater( )

		AnimatedSprite.Update( self, frame_time, ticks )




# -------- Enemy Tree --------
class EnemyTree( AnimatedSprite ):
	energy_up_rate = 1
	spawn_wait = 12000 # 6 seconds
	

	# Init
	def __init__( self, vector ):
		self.groups = Config.app.sprite_groups['enemy-trees'], Config.app.sprites_all
		self._layer = Config.sprite_layer_enemies

		AnimatedSprite.__init__( self, "enemies/tree-1.png", vector )

		self.level = 1
		self.energy = 1.0
		self.last_spawn = self.spawn_wait

		self.AddAnimationState( "idle", 0, 5, 6 )
		self.SetAnimationState( "idle" )

		#Config.app.em.RegisterListener( FriendlyTreePlayerCollisionListener() )


	# Update
	def Update( self, frame_time, ticks ):
		m = frame_time / 1000.0

		self.energy += (self.energy_up_rate * m)

		if self.energy > 30:
			self.level = 2
			self.ReloadSrc( "enemies/tree-2.png" )

		if self.level == 2:
			if self.last_spawn <= 0:
				self.last_spawn = self.spawn_wait
				r = 1 + int(self.energy / 120)
				for i in range(r):
					EnemyFlying( self.vector )
			else:
				self.last_spawn -= frame_time

		AnimatedSprite.Update( self, frame_time, ticks )




# -------- Enemy Flying --------
class EnemyFlying( MovingSprite ):
	max_speed 	= [300.0, 200.0] # Pixels per second
	accl 		= [10.0, 5.0] # Change per second
	dccl		= [5.0, 5.0]
	spawn_wait = 10000 # Every 10 seconds

	# Init
	def __init__( self, vector ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['enemy-flying'], Config.app.sprites_all
		self._layer = Config.sprite_layer_enemies

		# Create as animated sprite
		MovingSprite.__init__(
			self,
			"enemies/flying-1.png",
			vector
		)

		self.direction = 1
		if random.randint(0,1): self.direction = -1

		self.cur_speed 	= [self.direction * float(random.randint(0, 600)), -float(random.randint(500, 800))]
		self.is_accl 	= [0, 0]
		self.move_vector = [0, 0]
		self.spawning = False
		self.last_spawn = 0
		self.target = False
		self.level = -1
		self.health = 2

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
		
		if self.target == False:
			self.target = self.FindNearestFriendlyPlant( )

		if self.target == False:
			# Roam
			self.is_accl[0] = self.direction

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
	def Spawn( self, r=None ):

		if r == None:
			r = self.level * 5

		for i in range( r ):
			EnemySpore( Vector2D.AddVectors(self.vector, [self.rect.w/2, 0]) )

		# Level up
		self.level += 1
		if self.level > 4:
			self.level = 4
		else:
			if self.level > 1:
				self.health = self.level * 2
				self.ReloadSrc( "enemies/flying-"+str(self.level)+".png" )

	# Die Overly Dramtically
	def DieOverlyDramatically( self ):
		self.Spawn( 1 )
		if self.target:
			self.target.targeted = False
			self.target.targeted_by = None

		dist_to_player = abs(self.vector[0] - Config.player.vector[0])
		if dist_to_player == 0: dist_to_player = 1
		volume = 100.0 / float(Config.screen_w * Config.world_size)
		volume = volume * (float(Config.screen_w * Config.world_size) - float(dist_to_player * 1.5))
		if volume < 0: volume = 1.0
		volume = volume / 200.0
		sound_die.set_volume( volume )

		sound_die.play( )

		self.kill( )

	# Update
	def Update( self, frame_time, ticks ):
		MovingSprite.Update( self, frame_time, ticks )

		if self.vector[1] < random.randint(25,80):
			self.is_accl[1] = 1
		else:
			self.is_accl[1] = 0

		if self.vector[0] <= 40:
			self.direction = 1
		elif self.vector[0] >= (Config.screen_w * Config.world_size) - 40:
			self.direction = -1

		self.MoveToNearestFriendlyPlant( frame_time )