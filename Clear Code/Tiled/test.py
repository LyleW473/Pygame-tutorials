import pygame, sys
from pytmx.util_pygame import load_pygame


class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, surf):
		pygame.sprite.Sprite.__init__(self)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

pygame.init()
screen = pygame.display.set_mode((1280,720))
tmx_data = load_pygame('data/tmx/basic.tmx')
sprite_group = pygame.sprite.Group()

# Cycle through all layers
for layer in tmx_data.visible_layers:
	#if layer.name in ('Floor', 'Plants and rocks', 'Pipes'):
	if hasattr(layer, 'data'):
		for x, y, surf in layer.tiles():
			pos = (x * 128, y * 128)
			tiles = Tile(pos = pos, surf = surf)
			sprite_group.add(tiles)


for obj in tmx_data.objects:
	pos = (obj.x, obj.y)
	# if obj.image:
	if obj.type in ('Building', 'Vegetation'):
		Tile(pos = pos, surf = obj.image, groups = sprite_group)
	
# Get layers
#print(tmx_data.layers) # Get all layers
#for layer in tmx_data.visible_layers: # Get visible layers
#	print(layer)

#print(tmx_data.layernames) # Get all layer names as dictionary
#print(tmx_data.get_layer_by_name('Floor')) # Get one layer by name

#for obj in tmx_data.objectgroups: # Get object layers
#	print(obj)

# Get tiles
#layer = tmx_data.get_layer_by_name('Floor')
#for x, y, surf in layer.tiles(): # For each tile in the tile generator. Each tile has an (x, y, surface). Get all the information for tiles
#	print(x * 128)
#	print(y * 128)
#	print(surf)

# Get objects
#object_layer = tmx_data.get_layer_by_name('Objects')
#for obj in object_layer:
#	print(obj.x)
#	print(obj.y)
#	print(obj.image)
#	if obj.type == 'Shape':
#		if obj.name == 'Marker': 
#			print(obj.x)
#			print(obj.y)
#		if obj.name == 'Rectangle':
#			print(obj)
#			print(obj.x)
#			print(obj.y)
#			print(obj.width)
#			print(obj.height)
#			print(obj.as_points)
#		if obj.name == 'Ellipse':
#			print(dir(obj))
#		if obj.name == 'Polygon':
#			print(obj.as_points) # Returns boundary points
#			print(obj.points) # Returns points of the corners of the polygon


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('black')
	sprite_group.draw(screen)

	pygame.display.update()