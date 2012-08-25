# -------- Sprite.py --------
# Handles sprites
# ---------------------------

# Imports
import pygame
import Vector2D

# Definitions
folder = "sprites/"


# -------- Static Sprite --------
class StaticSprite( pygame.sprite.Sprite ):
	visible = True
	image_angle = False

	# Init
	def __init__( self, src, vector ):
		pygame.sprite.Sprite.__init__( self, self.groups )

		self.vector = vector
		self.image = pygame.image.load( folder+src ).convert_alpha( )
		self.rect = self.image.get_rect( )
		self.rect.x = vector[0]
		self.rect.y = vector[1]


	# Update
	def Update( self, frame_time, ticks ):
		self.rect.x = self.vector[0]
		self.rect.y = self.vector[1]



# -------- Animated Sprite --------
class AnimatedSprite( pygame.sprite.Sprite ):
	loaded = False
	visible = True
	image_angle = False

	# Init
	def __init__( self, src, vector ):
		pygame.sprite.Sprite.__init__( self, self.groups )

		self.images = [ ]
		self.frames = 0
		self.states = { }
		self.vector = vector

		self.src_image = pygame.image.load( folder+src ).convert_alpha( )
		self.src_width, self.src_height = self.src_image.get_size( )

		self._last_update = 0
		self._frame = 0
		self.state = ''


	# Add Animation State
	def AddAnimationState( self, name, start, end, fps ):
		self.frames += (end - start + 1)
		self.states[ name ] = {
			'start': start,
			'end': end,
			'delay': ( 1000 / fps )
		}


	# Set Animation State
	def SetAnimationState( self, name ):
		# If not current state
		if self.state != name:
			# Check if the files have been loaded
			if self.loaded == False:
				# Calculate frame width and split frames
				self.frame_width = self.src_width / self.frames
				for i in range( self.frames ):
					self.images.append( self.src_image.subsurface(i * self.frame_width, 0, self.frame_width, self.src_height) )

				# Set image
				self.image = self.images[0]
				self.rect = self.image.get_rect( )
				self.rect.x = self.vector[0]
				self.rect.y = self.vector[1]

			# Set state
			self.state = name
			self._frame = self.states[name]['start']
			self._last_update = 0


	# Update Animation
	def UpdateAnimation( self, ticks ):
		# Get current state
		state = self.states[self.state]

		# Update vector position
		self.rect.x = self.vector[0]
		self.rect.y = self.vector[1]

		# Check if enough ticks have passed to update animation
		if ticks - self._last_update > state['delay']:
			frame = self._frame
			self._frame += 1

			# Wrap frame between state start and end
			if self._frame < state['start']: self._frame = state['start']
			if self._frame > state['end']:   self._frame = state['start']

			#if self._frame != frame:
				# Update image
			self.image = self.images[self._frame]
			self._last_update = ticks

			# Update angle
			if self.image_angle != False:
				self.image = pygame.transform.rotate( self.image, self.image_angle )


	# Update
	def Update( self, frame_time, ticks ):
		self.UpdateAnimation( ticks )



# -------- Moving Sprite --------
class MovingSprite( AnimatedSprite ):
	max_speed 	= [100.0, 100.0] # Pixels per second
	cur_speed 	= [0.0, 0.0]
	accl 		= [20.0, 20.0] # Change per second
	dccl		= [10.0, 10.0]
	is_accl 	= [0, 0]

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


	# Update
	def Update( self, frame_time, ticks ):
		AnimatedSprite.Update( self, frame_time, ticks )
		self.Move( frame_time )