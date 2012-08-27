# -------- Config.py --------
# Shared configuration
# ---------------------------

# General Information
app_title = "Neon Spores"
fps = 60

# Sprite Layers
sprite_layer_player = 1
sprite_layer_enemies = 2
sprite_layer_friendlies = 3
sprite_layer_terrain = 4

# World
world_size = 4
world_offset = 0

# Colours
colour_player = (115, 241, 255)
colour_friendly = (111, 255, 0)
colour_enemy = (255, 0, 208)

# Shared Objects
app = None
screen = None
player = None
world = None

enemies = []