# -------- Friendly.py --------
# Handles all logic relating to the friendlies
# -----------------------------

# Imports
import random
import Config, Vector2D
from Sprite import AnimatedSprite, MovingSprite

# -------- Friendly --------
class FriendlySpore( MovingSprite ):
	pass

class FriendlyBug( AnimatedSprite ):
	gravity = 400.0 # fall pixels per second

	# Init
	def __init__( self ):
		# Set groups & layer
		self.groups = Config.app.sprite_groups['friendly'], Config.app.sprites_all
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

	# Update
	def Update( self, frame_time, ticks ):
		m = frame_time / 1000.0

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

		AnimatedSprite.Update( self, frame_time, ticks )