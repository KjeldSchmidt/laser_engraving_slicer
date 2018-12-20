from typing import List, Tuple
from PIL import Image, ImageDraw, ImageQt
from PyQt5 import QtGui


def extract_new_position( line: str, pixels_per_mm ) -> Tuple[ float, float ]:
	x = float( list( filter( lambda x: x[ 0 ] == 'X', line.split() ) )[ 0 ][ 1: ] ) * pixels_per_mm
	y = float( list( filter( lambda x: x[ 0 ] == 'Y', line.split() ) )[ 0 ][ 1: ] ) * pixels_per_mm
	return x, y


def image_from_gcode( gcode: str, pixels_per_mm=5 ):
	lines = gcode.splitlines()
	lines = lines[ 6: ]

	max_y = find_max_y( lines )
	max_x = find_max_x( lines )

	height = int( max_y * pixels_per_mm )
	width = int( max_x * pixels_per_mm )

	image = Image.new( 'L', (width, height), 255 )
	draw = ImageDraw.Draw( image )

	fill = False
	cur_x = 0
	cur_y = 0
	for line in lines:
		if line == 'M106 S255':
			fill = True

		elif line == 'M106 S0':
			fill = False

		else:
			new_x, new_y = extract_new_position( line, pixels_per_mm )
			if fill:
				draw.line( (cur_x, cur_y, new_x, new_y), 0 )
			cur_x, cur_y = new_x, new_y
	qim = ImageQt.ImageQt( image )
	image = QtGui.QPixmap.fromImage( qim )
	return image


def find_max_y( gcode: List[ str ] ):
	moves = filter( lambda x: 'G0' in x or 'G1' in x, gcode )
	y_moves = filter( lambda x: 'Y' in x, moves )
	y_positions = map( lambda x: x.split()[ 2 ], y_moves )
	y_positions_float = map( lambda x: float( x[ 1: ] ), y_positions )
	return max( y_positions_float )


def find_max_x( gcode: List[ str ] ):
	moves = filter( lambda x: 'G0' in x or 'G1' in x, gcode )
	x_moves = filter( lambda x: 'X' in x, moves )
	x_positions = map( lambda x: x.split()[ 1 ], x_moves )
	x_positions_float = map( lambda x: float( x[ 1: ] ), x_positions )
	return max( x_positions_float )
