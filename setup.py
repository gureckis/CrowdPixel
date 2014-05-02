import image_slicer

tiles = image_slicer.slice('brain.png',600, save=False)
image_slicer.save_tiles(tiles, prefix='tile', directory='static/images/tiles', format='png')

# add number of tiles to config.txt
