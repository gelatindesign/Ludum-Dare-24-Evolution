# -------- Sprite.py --------
# Handles sprites
# ---------------------------

# Imports
import pygame

# Definitions
folder = "sprites/"
scale = 2


# -------- Static Sprite --------
class StaticSprite( pygame.sprite.Sprite ):
	visible = True
	image_angle = False

	# Init
	def __init__( self, src, vector, layer ):
		pygame.sprite.Sprite.__init__( self )

		self.image = pygame.image.load( src ).convert_alpha( )



# -------- Animated Sprite --------
class AnimatedSprite( pygame.sprite.Sprite ):
	loaded = False
	visible = True
	image_angle = False

	# Init
	def __init__( self, src, vector, layer ):
		pygame.sprite.Sprite.__init__( self, self.groups )

		self.images = [ ]
		self.frames = 0
		self.states = { }
		self.vector = vector
		self.layer = layer

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

			if self._frame != frame:
				# Update image
				self.image = self.images[self._frame]
				self._last_update = ticks

			# Update angle
			if self.image_angle != False:
				self.image = pygame.transform.rotate( self.image, self.image_angle )