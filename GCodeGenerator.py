from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage

_CMD_laser_on = 'M106 S255'
_CMD_laser_off = 'M106 S0'


def initialize_printer( settings: Dict ) -> str:
	x_init = settings[ 'x_init' ]
	y_init = settings[ 'y_init' ]
	move_z = settings[ 'move_z_axis' ]
	z_init = settings[ 'focal_length' ] + settings[ 'plate_height' ]
	feed_rate = settings[ 'move_speed' ]

	if move_z:
		initial_position_line = \
			f'G1 X{x_init:.2f} Y{y_init:.2f} Z{z_init:.2f} ; Move laser to lower left corner of printing bed'
		homing_line = 'G28 ; Home all axes.'
	else:
		initial_position_line = f'G1 X{x_init:.2f} Y{y_init:.2f} ; Move laser to lower left corner of printing bed'
		homing_line = 'G28 X Y; Home all axes.'

	initial_lines = [
		'G90 ; Set coordinate system to absolute values in X, Y, Z',
		'M106 S0 ; Turn off the laser',
		homing_line,
		initial_position_line,
		'G92 X0 Y0 ; Reset Coordinate System',
		f'G0 F{ feed_rate }'
	]

	return '\n'.join( initial_lines )


def finalize_printer( settings ) -> str:
	return _CMD_laser_off


def make_gcode( settings: Dict, image: QImage ) -> str:
	gcode = [ ]
	start = initialize_printer( settings )
	image_code = image_to_code( settings, image )
	end = finalize_printer( settings )

	gcode.append( start )
	gcode.append( image_code )
	gcode.append( end )

	return '\n'.join( gcode )


def image_to_code( settings: Dict, image: QImage ) -> str:
	height = image.height()
	width = image.width()

	pixel_box_size = settings[ 'pixel_box_size' ]

	instructions = [ ]

	for row_inv in range( height ):
		row = height - row_inv - 1
		for col in range( width ):
			color = image.pixelColor( row, col )
			if color == Qt.black:
				instructions.extend( [
					f'G1 X{col*pixel_box_size:.2f} Y{row*pixel_box_size:.2f}',
					_CMD_laser_on,
					f'G1 X{(col+1)*pixel_box_size:.2f} Y{row*pixel_box_size:.2f}',
					f'G1 X{(col+1)*pixel_box_size:.2f} Y{(row+1)*pixel_box_size:.2f}',
					f'G1 X{col*pixel_box_size:.2f} Y{(row+1)*pixel_box_size:.2f}',
					_CMD_laser_off,
					f'G1 X{(col+1)*pixel_box_size:.2f} Y{(row+1)*pixel_box_size:.2f}',
					_CMD_laser_on,
					f'G1 X{col*pixel_box_size:.2f} Y{row*pixel_box_size:.2f}',
					_CMD_laser_off,
					f'G1 X{(col+1)*pixel_box_size:.2f} Y{row*pixel_box_size:.2f}',
					_CMD_laser_on,
					f'G1 X{col*pixel_box_size:.2f} Y{(row+1)*pixel_box_size:.2f}',
				] )

	return '\n'.join( instructions )
