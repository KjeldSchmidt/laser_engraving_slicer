from typing import Dict, List

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPainter

_CMD_laser_on = 'M106 S255'
_CMD_laser_off = 'M106 S0'


def _initialize_printer( settings: Dict ) -> str:
	x_init = settings[ 'x_init' ]
	y_init = settings[ 'y_init' ]
	move_z = settings[ 'move_z_axis' ]
	z_init = settings[ 'focal_length' ] + settings[ 'plate_thickness' ]
	feed_rate = settings[ 'move_speed' ]

	if move_z:
		initial_position_line = \
			f'G1 X{x_init:.2f} Y{y_init:.2f} Z{z_init:.2f} ; Move laser to lower left corner of printing bed'
		homing_line = 'G28 ; Home all axes.'
	else:
		initial_position_line = f'G1 X{x_init:.2f} Y{y_init:.2f} ; Move laser to lower left corner of printing bed'
		homing_line = 'G28 X Y ; Home X and Y.'

	initial_lines = [
		'G90 ; Set coordinate system to absolute values in X, Y, Z',
		_CMD_laser_off,
		homing_line,
		initial_position_line,
		'G92 X0 Y0 ; Reset Coordinate System',
		f'G0 F{ feed_rate }'
	]

	return '\n'.join( initial_lines )


def _finalize_printer( settings ) -> str:
	return _CMD_laser_off


def make_gcode( settings: Dict, image: QImage ) -> str:
	gcode = [ ]
	start = _initialize_printer( settings )
	end = _finalize_printer( settings )

	if settings[ 'burn_style' ] == 0:
		image_code = _image_to_bw_crosses( settings, image )
	elif settings[ 'burn_style' ] == 1:
		image_code = _image_to_parallel_lines_( settings, image )

	gcode.append( start )
	gcode.append( image_code )
	gcode.append( end )

	return '\n'.join( gcode )


def _image_to_parallel_lines_( settings: Dict, image: QImage ) -> str:
	scaled_image = _scale_image( settings, image )
	image = scaled_image.convertToFormat( QImage.Format_Grayscale8 )


def _image_to_bw_crosses( settings: Dict, image: QImage ) -> str:
	scaled_image = _scale_image( settings, image )
	image = scaled_image.convertToFormat( QImage.Format_Mono )

	height = image.height()
	width = image.width()

	instructions = [ ]

	for row_inv in range( height ):
		row = height - row_inv - 1
		for col in range( width ):
			color = image.pixelColor( col, row )
			if color == Qt.black:
				instructions.extend( _fill_square( settings, row, col ) )

	return '\n'.join( instructions )


def _fill_square( settings: Dict, row: int, col: int ) -> List[ str ]:
	pixel_box_size = settings[ 'pixel_box_size' ]

	return [
		f'G0 X{col * pixel_box_size:.2f} Y{row * pixel_box_size:.2f}',
		_CMD_laser_on,
		f'G1 X{(col + 1) * pixel_box_size:.2f} Y{row * pixel_box_size:.2f}',
		f'G1 X{(col + 1) * pixel_box_size:.2f} Y{(row + 1) * pixel_box_size:.2f}',
		f'G1 X{col * pixel_box_size:.2f} Y{(row + 1) * pixel_box_size:.2f}',
		f'G0 X{col * pixel_box_size:.2f} Y{row * pixel_box_size:.2f}',
		f'G0 X{(col + 1) * pixel_box_size:.2f} Y{(row + 1) * pixel_box_size:.2f}',
		_CMD_laser_off,
		f'G1 X{(col + 1) * pixel_box_size:.2f} Y{row * pixel_box_size:.2f}',
		_CMD_laser_on,
		f'G1 X{col * pixel_box_size:.2f} Y{(row + 1) * pixel_box_size:.2f}',
		_CMD_laser_off
	]


def _scale_image( settings: Dict, source_image: QImage ):
	source_image_width = source_image.width()
	source_image_height = source_image.height()
	source_image_ratio = source_image_height / source_image_width

	pixel_box_size = settings[ 'pixel_box_size' ]
	plate_width = settings[ 'plate_width' ]
	plate_height = settings[ 'plate_height' ]

	result_image_width = int( plate_width / pixel_box_size )
	result_image_height = int( plate_height / pixel_box_size )
	result_image_ratio = result_image_height / result_image_width

	result = QImage( result_image_width, result_image_height, source_image.format() )

	if source_image_ratio < result_image_ratio:
		scaled_image = source_image.scaledToWidth( result_image_width )
		position = QPoint( 0, result_image_height / 2 - scaled_image.height() / 2 )
	else:
		scaled_image = source_image.scaledToHeight( result_image_height )
		position = QPoint( result_image_width / 2 - scaled_image.width() / 2, 0 )

	result.fill( Qt.white )

	painter = QPainter( result )
	painter.drawImage( position, scaled_image )
	painter.end()

	return result
