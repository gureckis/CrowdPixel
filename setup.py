import image_slicer
import os
from psiturk.db import db_session, init_db, Base
from custom_models import Pixels

init_db()  # initialze the data base, creating tables for the custom_models.py if necessary

TILEPATH = './static/images/tiles/'
TARGETFILE = 'brain.png'
NTILES = 16

# first delete all the files in the static/images/tiles folder
files = os.listdir(TILEPATH)
for myfile in files:
	if myfile != 'placeholder.txt':
		print "removing existing file", TILEPATH+myfile
		os.remove(TILEPATH+myfile)

# query existing pixels
Pixels.query.delete()

# create the tiles using the target image
tiles = image_slicer.slice(TARGETFILE, NTILES, save=False)
image_slicer.save_tiles(tiles, prefix='tile', directory='static/images/tiles', format='png')

# add tiles to database
for tile in tiles:
	pixel_width, pixel_height = tile.image.size
	print "dimensions:", (pixel_width, pixel_height) , "filename:", tile.filename
	pixel_attributes = dict(filename = tile.filename,
								n_completed = 0,
								width = pixel_width,
								height = pixel_height)
	pixel = Pixels(**pixel_attributes)
	db_session.add(pixel)
	db_session.commit()

